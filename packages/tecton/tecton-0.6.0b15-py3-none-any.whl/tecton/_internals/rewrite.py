from typing import Dict
from typing import List
from typing import Optional

import attrs
import pendulum
import pyspark
from pyspark.sql import SparkSession

from tecton._internals.data_frame_helper import _get_time_limits_of_dataframe
from tecton._internals.feature_views import aggregations
from tecton_core import conf
from tecton_core.pipeline_common import get_time_window_from_data_source_node
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import AddEffectiveTimestampNode
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import FullAggNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import PartialAggNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import RespectFSTNode
from tecton_core.query.rewrite import Rewrite
from tecton_spark.query import translate


class MockDataRewrite(Rewrite):
    """
    Replace DataSourceScanNode with MockDataSourceScanNode based on DataSource ID map.
    """

    def __init__(self, mock_data: Dict[str, NodeRef]):
        self.mock_data = mock_data

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, DataSourceScanNode):
            node = tree.node
            if node.ds.id in self.mock_data:
                # Replace with mock data
                tree.node = MockDataSourceScanNode(
                    self.mock_data[node.ds.id],
                    node.ds,
                    self.mock_data[node.ds.id].columns,
                    node.start_time,
                    node.end_time,
                )
        else:
            for i in tree.inputs:
                self.rewrite(i)


class SpineEntityPushdown(Rewrite):
    """Filters the original feature data with respect to the entities contained in a spine.

    Requires a Spark session since the spine must be evaluated.

    This should be applied to AsofJoinNodes and FullAggNodes since both of have sorts (as part of windows), for which
    we would like to minimize memory usage.
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, FullAggNode):
            self.rewrite_full_agg(tree)
        elif isinstance(tree.node, AsofJoinFullAggNode):
            self.rewrite_asof_full_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef):
        node = tree.node
        # In our current usage of AsofJoinNode, we always pass in the spine on the left.
        spine = translate.spark_convert(node.left_container.node).to_dataframe(self.spark)
        self.pushdown_entities(node.right_container.node, spine, node.join_cols)

    def rewrite_full_agg(self, tree: NodeRef):
        node = tree.node
        # We should only rewrite if the FullAggNode actually has a spine.
        if node.spine is not None:
            spine = translate.spark_convert(node.spine).to_dataframe(self.spark)
            self.pushdown_entities(node.input_node, spine, node.fdw.join_keys)

    def rewrite_asof_full_agg(self, tree: NodeRef):
        node = tree.node
        spine = translate.spark_convert(node.spine).to_dataframe(self.spark)
        self.pushdown_entities(node.partial_agg_node, spine, node.fdw.join_keys)

    def pushdown_entities(self, tree: NodeRef, spine: pyspark.sql.DataFrame, join_cols: List[str]):
        node = tree.node
        can_be_pushed_down = (
            RespectFSTNode,
            RenameColsNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
            PartialAggNode,
        )
        if isinstance(node, can_be_pushed_down):
            self.pushdown_entities(node.input_node, spine, join_cols)
        else:
            # We could consider caching this
            spine_entities = spine.select(join_cols).distinct()
            entities_node = DataNode(data=spine_entities, cols=join_cols).as_ref()
            tree.node = EntityFilterNode(node.as_ref(), entities_node, join_cols)


# TODO: genericize this so it can be applied to non-spark. Right now we depend on directly being able to read dataframe from spark to get time limits.
class SpineTimePushdown(Rewrite):
    """
    We actually evaluate the spine to get the time ranges for this rewrite, so we need a spark session to do so.
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark
        # The spine time limits are the same for all spines used throughout the query, so we only calculate once.
        self.spine_time_limits: Optional[pendulum.Period] = None

    def rewrite(self, tree: NodeRef):
        if isinstance(tree.node, FullAggNode):
            self.rewrite_agg(tree)
        elif isinstance(tree.node, AsofJoinNode):
            self.rewrite_asof(tree)
        elif isinstance(tree.node, AsofJoinFullAggNode):
            self.rewrite_asof_full_agg(tree)
        else:
            for i in tree.inputs:
                self.rewrite(i)

    def rewrite_asof(self, tree: NodeRef):
        node = tree.node
        # In our current usage of the code, we always pass in the spine on the left side of the asof join.
        # This rewrite is still applicable for any type of dataframe on the left, but referring to it as spine
        # to make the naming match up with the aggregate case (in which the spine is not on the left).
        if self.spine_time_limits is None:
            spine = translate.spark_convert(node.left_container.node).to_dataframe(self.spark)
            self.spine_time_limits = _get_time_limits_of_dataframe(spine, node.left_container.timestamp_field)
        self.pushdown_time_range(node.right_container.node, self.spine_time_limits)

    # Compute the time limits from the node, and push down the time limits to its input
    def rewrite_agg(self, tree: NodeRef):
        node = tree.node
        # Spines are optional on the aggregate nodes.
        if node.spine is not None:
            if self.spine_time_limits is None:
                spine = translate.spark_convert(node.spine).to_dataframe(self.spark)
                self.spine_time_limits = _get_time_limits_of_dataframe(spine, node.fdw.time_key)
            self.pushdown_time_range(node.input_node, self.spine_time_limits)

    # Compute the time limits from the node, and push down the time limits to its input
    def rewrite_asof_full_agg(self, tree: NodeRef):
        node = tree.node
        if self.spine_time_limits is None:
            spine = translate.spark_convert(node.spine).to_dataframe(self.spark)
            self.spine_time_limits = _get_time_limits_of_dataframe(spine, node.fdw.time_key)
        self.pushdown_time_range(node.partial_agg_node, self.spine_time_limits)

    # Push down and convert spine time filter to either raw data or feature time filter at the DataSourceScanNode or OfflineStoreScanNode.
    # Nodes that do not affect the correlation with the spine time range are enumerated in the can_be_pushed_down list.
    def pushdown_time_range(self, tree: NodeRef, spine_time_limits: pendulum.Period):
        node = tree.node
        can_be_pushed_down = (
            RespectFSTNode,
            RenameColsNode,
            PartialAggNode,
            FeatureTimeFilterNode,
            AddAnchorTimeNode,
            AddDurationNode,
            AddEffectiveTimestampNode,
        )
        if isinstance(node, can_be_pushed_down):
            self.pushdown_time_range(node.input_node, spine_time_limits)
        elif isinstance(node, (OfflineStoreScanNode, FeatureViewPipelineNode)):
            # NB: don't use aggregations._get_feature_time_limits; it does not account for aggregation windows.
            feature_time_limits = aggregations._get_time_limits(
                fd=node.feature_definition_wrapper, spine_df=None, spine_time_limits=spine_time_limits
            )
            # TODO: have the above returned time limits be appropriate for feature tables
            if node.feature_definition_wrapper.is_feature_table:
                feature_time_limits = feature_time_limits.end - (
                    feature_time_limits.start - node.feature_definition_wrapper.serving_ttl
                )
            if isinstance(node, FeatureViewPipelineNode):
                # swap the pipeline node to add new time limits
                node = FeatureViewPipelineNode(node.inputs_map, node.feature_definition_wrapper, feature_time_limits)
                tree.node = node

                for n in node.inputs:
                    if isinstance(n.node, DataSourceScanNode):
                        # this method will convert aligned_feature_time_limits to raw data time limits by accounting for FilteredSource offsets etc.
                        data_time_filter = get_time_window_from_data_source_node(
                            feature_time_limits,
                            node.feature_definition_wrapper.batch_materialization_schedule,
                            n.node.ds_node,
                        )
                        if data_time_filter is not None:
                            n.node = attrs.evolve(
                                n.node, start_time=data_time_filter.start, end_time=data_time_filter.end
                            )
            elif isinstance(node, OfflineStoreScanNode):
                tree.node = attrs.evolve(node, time_filter=feature_time_limits)


# Mutates the input
def rewrite_tree_for_spine(tree: NodeRef, spark: SparkSession):
    if not conf.get_bool("QUERY_REWRITE_ENABLED"):
        return
    rewrites = [SpineTimePushdown(spark), SpineEntityPushdown(spark)]
    for rewrite in rewrites:
        rewrite.rewrite(tree)
