from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
import pypika
from pypika import AliasedQuery
from pypika import analytics as an
from pypika import Case
from pypika import Database
from pypika import Field
from pypika import Interval
from pypika import NULL
from pypika import Query
from pypika import Table
from pypika.terms import LiteralValue

from tecton_core import specs
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.pipeline_common import PipelineSqlBuilder
from tecton_core.query.node_interface import INDENT_BLOCK
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.sql_compat import CustomQuery
from tecton_core.query.sql_compat import date_add
from tecton_core.query.sql_compat import from_unixtime
from tecton_core.query.sql_compat import LastValue
from tecton_core.query.sql_compat import Query
from tecton_core.query.sql_compat import to_timestamp
from tecton_core.query.sql_compat import to_unixtime
from tecton_core.time_utils import convert_duration_to_seconds
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy

EFFECTIVE_TIMESTAMP = "_effective_timestamp"
EXPIRATION_TIMESTAMP = "_expiration_timestamp"


@attrs.frozen
class OdfvPipelineNode(QueryNode):
    """
    Evaluates an odfv pipeline on top of an input containing columns prefixed '_udf_internal' to be used as dependent feature view inputs. The _udf_internal contract is
    documented in pipeline_helper.py
    The input may also have other feature values. This ensures we can match multiple odfv features to the right rows based on request context without joining them.
    In order to make this possible, a namespace is also passed through at this point to ensure the odfv features do not conflict with other features.
    """

    input_node: NodeRef
    feature_definition_wrapper: FeatureDefinitionWrapper
    namespace: str

    @property
    def columns(self) -> Tuple[str, ...]:
        sep = self.feature_definition_wrapper.namespace_separator
        return tuple(
            list(self.input_node.columns)
            + [f"{self.namespace}{sep}{name}" for name in self.feature_definition_wrapper.view_schema.column_names()]
        )

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return f"Evaluate OnDemand Pipeline: {self.feature_definition_wrapper.name}\n"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class FeatureViewPipelineNode(QueryNode):
    inputs_map: Dict[str, NodeRef]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.feature_definition_wrapper.view_schema.column_names()

    @property
    def schedule_interval(self) -> pendulum.Duration:
        # Note: elsewhere we set this to pendulum.Duration(seconds=fv_proto.materialization_params.schedule_interval.ToSeconds())
        # but that seemed wrong for bwafv
        return self.feature_definition_wrapper.batch_materialization_schedule

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple(self.inputs_map.values())

    def as_str(self, verbose: bool):
        s = f"Evaluate Pipeline: {self.feature_definition_wrapper.name}"
        if verbose:
            s += f" with feature_time_limits {self.feature_time_limits}"
        s += "\n"
        return s

    def pretty_print(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ) -> str:
        # Build string representation of this node.
        s = self.pretty_print_self(verbose, indents, indent_block, show_ids, names_only)

        # Count the number of leading spaces.
        first_line = s.split("\n")[0]
        num_leading_spaces = len(first_line) - len(first_line.lstrip())

        # Recursively add ancestors.
        for k in self.inputs_map:
            # Add whitespace to match the number of leading spaces, then the name of the input.
            s += " " * num_leading_spaces
            s += f"- PipelineInput: {k}\n"

            # Then add the ancestor.
            s += self.inputs_map[k].pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)
        return s

    def _to_query(self) -> pypika.Query:
        # maps input names to unique strings
        unique_inputs_map = {k: f"{k}_{id(self)}" for k in self.inputs_map}
        queries = PipelineSqlBuilder(
            pipeline=self.feature_definition_wrapper.pipeline,
            id_to_transformation={t.id: t for t in self.feature_definition_wrapper.transformations},
            materialization_context=BoundMaterializationContext._create_from_period(
                self.feature_time_limits,
                self.schedule_interval,
            ),
            renamed_inputs_map=unique_inputs_map,
        ).get_queries()
        # the base query is the query from the root of the pipeline (at the end of the list)
        res = CustomQuery(queries[-1][0])
        # add CTE for each of the inputs, aliased to the unique name
        for k in unique_inputs_map:
            res = res.with_(self.inputs_map[k]._to_query(), unique_inputs_map[k])
        for t_node in queries[:-1]:
            query, alias = t_node
            res = res.with_(CustomQuery(query), alias)
        return res


@attrs.frozen
class DataSourceScanNode(QueryNode):
    """
    DataSource + Filter
    We don't have a separate filter node to hide away the filter/partition interaction with raw_batch_translator
    """

    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]  # value is set when used as an input to FV
    is_stream: bool = attrs.field()
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            # TODO(brian) - mypy complains this is a Tuple[Any,...]
            return tuple(str(f.name) for f in self.ds.stream_source.spark_schema.fields)
        elif self.ds.type == DataSourceType.PUSH:
            return tuple(str(f.name) for f in self.ds.schema.tecton_schema.columns)
        elif self.ds.type == DataSourceType.BATCH:
            return tuple(str(f.name) for f in self.ds.batch_source.spark_schema.fields)
        else:
            raise NotImplementedError

    # MyPy has a known issue on validators https://mypy.readthedocs.io/en/stable/additional_features.html#id1
    @is_stream.validator  # type: ignore
    def check_no_time_filter(self, _, is_stream: bool):
        if is_stream and (self.start_time is not None or self.end_time is not None):
            raise ValueError("Raw data filtering cannot be run on a stream source")

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self, verbose: bool):
        s = ""
        if self.start_time is not None or self.end_time is not None:
            s += f"TimeFilter: {self.start_time}:{self.end_time}\n"
        verb = "Read Stream" if self.is_stream else "Scan DataSource"
        s += f"{verb}: {self.ds.name}\n"
        return s

    def _to_query(self) -> pypika.Query:
        if self.is_stream:
            raise NotImplementedError
        source = self.ds.batch_source
        if hasattr(source, "table") and source.table:
            from_str = Database(source.database)
            if hasattr(source, "schema") and source.schema:
                from_str = from_str.__getattr__(source.schema)
            from_str = from_str.__getattr__(source.table)
        elif hasattr(source, "query") and source.query:
            from_str = CustomQuery(source.query)
        else:
            raise NotImplementedError
        return Query().from_(from_str).select("*")


@attrs.frozen
class RawDataSourceScanNode(QueryNode):
    """
    DataSource + Filter
    We don't have a separate filter node to hide away the filter/partition interaction with raw_batch_translator
    """

    ds: specs.DataSourceSpec

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(f.name for f in self.ds.batch_source.spark_schema.fields)

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self, verbose: bool):
        s = ""
        verb = "Read Stream" if self.is_stream else "Scan DataSource (no post_processor)"
        s += f"{verb}: {self.ds.name}\n"
        return s

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class OfflineStoreScanNode(QueryNode):
    """
    Fetch values from offline store
    """

    feature_definition_wrapper: FeatureDefinitionWrapper
    time_filter: Optional[pendulum.Period] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        cols = self.feature_definition_wrapper.materialization_schema.column_names()
        if self.feature_definition_wrapper.is_temporal:
            # anchor time is not included in m13n schema for bfv/sfv
            cols.append("_anchor_time")
        return cols

    def as_str(self, verbose: bool):
        s = ""
        if self.time_filter is not None:
            s += f"TimeFilter: {self.time_filter}\n"
        s += f"Scan OfflineStore: {self.feature_definition_wrapper.name}"
        return s

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def _to_query(self) -> pypika.Query:
        fields = (
            self.feature_definition_wrapper.features
            + self.feature_definition_wrapper.join_keys
            + [self.feature_definition_wrapper.timestamp_key]
        )
        workspace_prefix = self.feature_definition_wrapper.workspace.replace("-", "_")
        where_conds = []
        if self.time_filter is not None:
            time_col = Field(self.feature_definition_wrapper.timestamp_key)
            where_conds = [
                time_col >= to_timestamp(self.time_filter.start),
                time_col < to_timestamp(self.time_filter.end),
            ]
        q = (
            Query()
            .from_(Table(f"{workspace_prefix}__{self.feature_definition_wrapper.name}"))
            .select(*[Field(k) for k in fields])
        )
        for w in where_conds:
            q = q.where(w)
        return q


@attrs.frozen
class JoinNode(QueryNode):
    """Join two inputs.

    Attributes:
        left: The left input of the join.
        right: The right input of the join.
        join_cols: The columns to join on.
        how: The type of join. For example, 'inner' or 'left'. This will be passed directly to pyspark.
    """

    left: NodeRef
    right: NodeRef
    join_cols: List[str]
    how: str

    @property
    def columns(self) -> Tuple[str, ...]:
        right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
        return tuple(list(self.left.columns) + list(right_nonjoin_cols))

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left, self.right)

    def as_str(self, verbose: bool):
        return f"{self.how.capitalize()} join" + (f" on {self.join_cols}:" if verbose else ":")

    def pretty_print(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ) -> str:
        """Overrides the default `pretty_print` method in order to customize it."""
        # Build string representation of this node.
        s = self.pretty_print_self(verbose, indents, indent_block, show_ids, names_only)

        # Count the number of leading spaces.
        first_line = s.split("\n")[0]
        num_leading_spaces = len(first_line) - len(first_line.lstrip())

        # Add whitespace to match the number of leading spaces, then the name of the input.
        s += " " * num_leading_spaces
        s += f"- left join input:\n"
        s += self.left.pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)

        s += " " * num_leading_spaces
        s += f"- right join input:\n"
        s += self.right.pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)

        return s

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class EntityFilterNode(QueryNode):
    """Filters the feature data by the entities with respect to a set of entity columns.

    Attributes:
        feature_data: The features to be filtered.
        entities: The entities to filter by.
        entity_cols: The set of entity columns to filter by.
    """

    feature_data: NodeRef
    entities: NodeRef
    entity_cols: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.feature_data.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.feature_data, self.entities)

    def as_str(self, verbose: bool):
        return f"Filter feature data by entities" + (f" with respect to {self.entity_cols}:" if verbose else ":")

    def pretty_print(
        self,
        verbose: bool = False,
        indents: int = 0,
        indent_block: str = INDENT_BLOCK,
        show_ids: bool = True,
        names_only: bool = False,
    ) -> str:
        """Overrides the default `pretty_print` method in order to customize it."""
        # TODO(felix): Refactor all the `pretty_print` methods.

        # Build string representation of this node.
        s = self.pretty_print_self(verbose, indents, indent_block, show_ids, names_only)

        # Count the number of leading spaces.
        first_line = s.split("\n")[0]
        num_leading_spaces = len(first_line) - len(first_line.lstrip())

        # Add whitespace to match the number of leading spaces, then the name of the input.
        s += " " * num_leading_spaces
        s += f"- feature data:\n"
        s += self.feature_data.pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)

        s += " " * num_leading_spaces
        s += f"- entities:\n"
        s += self.entities.pretty_print(verbose, indents + 1, indent_block, show_ids, names_only)

        return s

    def _to_query(self) -> pypika.Query:
        feature_data = self.feature_data._to_query()
        entities = self.entities._to_query()
        return Query().from_(feature_data).inner_join(entities).on_field(*self.entity_cols).select(*self.columns)


@attrs.frozen
class AsofJoinInputContainer:
    node: NodeRef
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str] = None
    prefix: Optional[str] = None


@attrs.frozen
class AsofJoinNode(QueryNode):
    """
    A "basic" asof join on 2 inputs
    """

    left_container: AsofJoinInputContainer
    right_container: AsofJoinInputContainer
    join_cols: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(
            list(self.left_container.node.columns)
            + [
                f"{self.right_container.prefix}_{col}"
                for col in self.right_container.node.columns
                if col not in (self.join_cols)
            ]
        )

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.left_container.node, self.right_container.node)

    def as_str(self, verbose: bool):
        # TODO: this is gonna look ugly
        return "Asof Join:"

    def _to_query(self) -> pypika.Query:
        ASOF_JOIN_TIMESTAMP_COL_1 = "_asof_join_timestamp_1"
        ASOF_JOIN_TIMESTAMP_COL_2 = "_asof_join_timestamp_2"
        left_df = self.left_container.node._to_query()
        right_df = self.right_container.node._to_query()
        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp <= spine timestamp.
        # The ASOF_JOIN_TIMESTAMP_COL_1 and ASOF_JOIN_TIMESTAMP_COL_2 columns will be used for sorting.
        left_name = self.left_container.node.node.__class__.__name__ + "_" + str(id(self.left_container.node))
        right_name = self.right_container.node.node.__class__.__name__ + "_" + str(id(self.right_container.node))
        left_df = (
            Query()
            .with_(left_df, left_name)
            .from_(AliasedQuery(left_name))
            .select(
                Table(left_name).star,
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
            )
        )
        right_df = (
            Query()
            .with_(right_df, right_name)
            .from_(AliasedQuery(right_name))
            .select(
                Field(self.right_container.effective_timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.right_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
                Table(right_name).star,
            )
        )

        # includes both fv join keys and the temporal asof join key
        timestamp_join_cols = [ASOF_JOIN_TIMESTAMP_COL_1, ASOF_JOIN_TIMESTAMP_COL_2]
        common_cols = self.join_cols + timestamp_join_cols
        left_nonjoin_cols = [col for col in self.left_container.node.columns if col not in common_cols]
        # we additionally include the right time field though we join on the left's time field.
        # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
        right_nonjoin_cols = [
            col for col in self.right_container.node.columns if col not in set(self.join_cols + timestamp_join_cols)
        ]
        left_full_cols = (
            [LiteralValue(True).as_("is_left")]
            + [Field(x) for x in common_cols]
            + [Field(x) for x in left_nonjoin_cols]
            + [NULL.as_(f"{self.right_container.prefix}_{x}") for x in right_nonjoin_cols]
        )
        right_full_cols = (
            [LiteralValue(False).as_("is_left")]
            + [Field(x) for x in common_cols]
            + [NULL.as_(x) for x in left_nonjoin_cols]
            + [Field(x).as_(f"{self.right_container.prefix}_{x}") for x in right_nonjoin_cols]
        )
        left_df = Query().from_(left_df).select(*left_full_cols)
        right_df = Query().from_(right_df).select(*right_full_cols)
        union = left_df.union(right_df)
        right_window_funcs = []
        for column_name in right_nonjoin_cols:
            right_window_funcs.append(
                LastValue(Field(f"{self.right_container.prefix}_{column_name}"))
                .over(*[Field(x) for x in self.join_cols])
                .orderby(*[Field(x) for x in timestamp_join_cols])
                .rows(an.Preceding(), an.CURRENT_ROW)
                .ignore_nulls()
                .as_(f"{self.right_container.prefix}_{column_name}")
            )

        # We use the right side of asof join to find the latest values to augment to the rows from the left side.
        # Then, we drop the right side's rows.
        res = Query().from_(union).select(*(common_cols + left_nonjoin_cols + right_window_funcs + [Field("is_left")]))
        res = (
            Query()
            .from_(res)
            .select(
                *(
                    common_cols
                    + left_nonjoin_cols
                    + [Field(f"{self.right_container.prefix}_{x}") for x in right_nonjoin_cols]
                )
            )
            .where(Field("is_left"))
        )
        return res


@attrs.frozen
class AsofJoinFullAggNode(QueryNode):
    """
    Asof join full agg rollup
    """

    spine: NodeRef
    partial_agg_node: NodeRef
    fdw: FeatureDefinitionWrapper

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.spine, self.partial_agg_node)

    def as_str(self, verbose: bool):
        # TODO: this is gonna look ugly
        return "Asof FullAgg Join:"

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.spine.columns) + self.fdw.features)

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class FullAggNode(QueryNode):
    """
    Performs full aggregations for each of the aggregates in fdw.trailing_time_window_aggregation.
    The full aggregations are applied for all the join keys in spine; otherwise new aggregations changed via
    expiring windows will not be generated.

    The resulting dataframe with contain all join keys in the spine.
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper = attrs.field()
    spine: Optional[NodeRef]
    respect_feature_start_time: bool

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.fdw.features + self.fdw.join_keys + ["_anchor_time"]

    @fdw.validator
    def check_is_aggregate(self, _, value):
        if not value.is_temporal_aggregate:
            raise ValueError("Cannot make a FullAggNode of a non-aggregate feature view")

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        if self.spine:
            return (
                self.spine,
                self.input_node,
            )
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if verbose:
            return (
                "FullAggNode: Set any feature values for rows with time < feature_start_time to null\n"
                + "Use window function to perform full aggregations; window range = agg.time_range range preceding -> current row\n"
                + "right-join against spine, with _anchor_time = aligned_spine_timestamp - 1 window, because raw data in a given time will only be accessible for retrieval by the end of the window. We also do some stuff to account for upstream_lateness, but we don't do anything to account for differences in slide_window and batch_schedule. And also this kind of assumes materialization happens instantaneously."
                if self.spine
                else "Perform Full Aggregates"
            )
        else:
            return "Perform Full Aggregates"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class PartialAggNode(QueryNode):
    """Performs partial aggregations.

    Should only be used on WAFVs.

    For non-continuous WAFV, the resulting dataframe will have an anchor time column that represents the start times of
    the tiles. For a continuous SWAFV, since there are no tiles, the resulting dataframe will have an anchor time column
    that is just a copy of the input timestamp column. And it will also call it "_anchor_time".

    Attributes:
        input_node: The input node to be transformed.
        fdw: The feature view to be partially aggregated.
        window_start_column_name: The name of the anchor time column.
        window_end_column_name: If set, a column will be added to represent the end times of the tiles, and it will
            have name `window_end_column_name`. This is ignored for continuous mode.
        aggregation_anchor_time: If set, it will be used to determine the offset for the tiles.
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        cols = self.fdw.materialization_schema.column_names()
        # TODO(Felix) this is janky
        if self.window_end_column_name is not None and not self.fdw.is_continuous:
            cols.append(self.window_end_column_name)
        return cols

    @fdw.validator
    def check_is_aggregate(self, _, value):
        if not value.is_temporal_aggregate:
            raise ValueError("Cannot construct a PartialAggNode using a non-aggregate feature view.")

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if verbose:
            actions = [
                "Perform partial aggregations (i.e. generates tiles that are not rolled up).",
                f'Add column "{self.window_start_column_name}" as the start time of tiles.',
            ]
            if self.window_end_column_name:
                actions.append(f'Add column "{self.window_end_column_name}" as the end time of tiles.')
            if self.aggregation_anchor_time:
                actions.append(
                    f'Align column "{self.fdw.timestamp_key}" to the offset determined by {self.aggregation_anchor_time}.'
                )
            return "\n".join(actions)
        else:
            return "Perform partial aggregations."

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class AddAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the batch materialization window.

    This is useful for preparing a dataframe for materialization, as the materialization logic requires an anchor time
    column for BFVs and BWAFVs. BWAFVs are handled as a special case elsewhere, so this node should only be used on
    BFVs. The anchor time is the start time of the materialization window, so it is calculated as
    window('timestamp_field', batch_schedule).start.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the feature timestamp field.
    """

    input_node: NodeRef
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns + ["_anchor_time"]

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if not verbose:
            return "Add anchor time column '_anchor_time' to represent the materialization window."

        return (
            "Add anchor time column '_anchor_time' to represent the materialization window.\n"
            f"It is calculated as window('{self.timestamp_field}', batch_schedule).start where batch_schedule = "
            f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds."
        )

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        secs = convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)
        anchor_field = (to_unixtime(Field(self.timestamp_field)) - to_unixtime(Field(self.timestamp_field)) % secs).as_(
            "_anchor_time"
        )
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*", anchor_field)


@attrs.frozen
class AddRetrievalAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the most recent features available for retrieval.

    This node should only be used on WAFVs.

    The column will be an epoch column with units determined by `feature_store_format_version`.

    For continuous SWAFV, features are not aggregated, so the anchor time column is simply a copy of the retrieval
    timestamp column.

    For non-continuous WAFV, features are aggregated in tiles, so the anchor time column represents the most recent tile
    available for retrieval. At time t, the most recent tile available for retrieval is equivalent to the most recent
    tile for which any feature row has an effective timestamp that is less than t. Thus for non-continuous WAFV, this
    node is conceptually the opposite of `AddEffectiveTimestampNode`.

    For example, consider feature retrieval for a BWAFV at time t. Let T = t - data_delay. Then the most recent
    materialization job ran at time T - (T % batch_schedule), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % batch_schedule) - tile_interval.

    Similarly, consider feature retrieval for a SWAFV at time T. Since there is no data delay, the most recent
    materialization job ran at time T - (T % tile_interval), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % tile_interval) - tile_interval.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
            Only used for SWAFVs.
        tile_interval: The tile interval for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the retrieval timestamp field.
        is_stream: If True, the WAFV is a SWAFV.
        data_delay_seconds: The data delay for the feature view, in seconds.
    """

    input_node: NodeRef
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: Optional[int] = 0

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + ["_anchor_time"])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if not verbose:
            return "Add anchor time column '_anchor_time' to represent the most recent tile available for retrieval."

        if self.is_stream:
            return (
                "Add anchor time column '_anchor_time' to represent the most recent tile available for retrieval.\n"
                "For a time t, let T = t - data_delay. Then the anchor time is calculated as T - (T % tile_interval) "
                f"- tile_interval where data_delay = {self.data_delay_seconds} seconds and tile_interval = "
                f"{convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds."
            )

        return (
            "Add anchor time column '_anchor_time' to represent the most recent tile available for retrieval.\n"
            "For a time t, let T = t - data_delay. Then the anchor time is calculated as T - (T % batch_schedule) "
            f"- tile_interval where data_delay = {self.data_delay_seconds} seconds and batch_schedule = "
            f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds and "
            f"tile_interval = {convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds."
        )

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class ConvertEpochToTimestampNode(QueryNode):
    """Convert epoch columns to timestamp columns.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_formats: A dictionary mapping column names to feature store format versions. Each column in this
            dictionary will be converted from epoch to timestamp. Its feature store format version determines whether
            the timestamp is in seconds or nanoseconds.
    """

    input_node: NodeRef
    feature_store_formats: Dict[str, int]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return (
            f"Convert columns {list(self.feature_store_formats.keys())} from epoch (either seconds or ns) to timestamp."
        )

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class RenameColsNode(QueryNode):
    """
    Rename columns according to `mapping`. No action is taken for columns mapped to `None`. Drop columns in `drop`.
    """

    input_node: NodeRef
    mapping: Optional[Dict[str, str]] = None
    drop: Optional[List[str]] = None

    @property
    def columns(self) -> Tuple[str, ...]:
        cols = self.input_node.columns
        assert cols is not None, self.input_node
        newcols = []
        for col in cols:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                newcols.append(self.mapping[col])
            else:
                newcols.append(col)
        return tuple(newcols)

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        actions = []
        if self.mapping:
            actions.append(f"Rename columns with map {self.mapping}.")
        if self.drop:
            actions.append(f"Drop columns {self.drop}.")
        if not actions:
            actions.append("No columns are renamed or dropped.")
        return " ".join(actions)

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        projections = []
        for col in self.input_node.columns:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                projections.append(Field(col).as_(self.mapping[col]))
            else:
                projections.append(Field(col))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*projections)


@attrs.frozen
class DataNode(QueryNode):
    """Arbitrary data container.

    The executor node will need to typecheck and know how to handle the type of mock data.
    """

    data: Any
    cols: Tuple[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.cols

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return tuple()

    def as_str(self, verbose: bool):
        if verbose:
            return f"User-provided Data: type:{self.data.__class__}"
        else:
            return "User-provided Data"

    def _to_query(self) -> pypika.Query:
        # data should implement some tmp-table creating interface. for now hardcode
        t = "TMP_SPINE_TABLE_717f9f244837b3c3"
        return Query().from_(Table(t)).select(*self.cols)


@attrs.frozen
class MockDataSourceScanNode(QueryNode):
    """
    DataSource + Filter
    We don't have a separate filter node to hide away the filter/partition interaction with raw_batch_translator
    """

    data: NodeRef
    ds: specs.DataSourceSpec
    columns: Tuple[str]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.data,)

    def as_str(self, verbose: bool):
        s = ""
        if self.start_time is not None or self.end_time is not None:
            s += f"TimeFilter: {self.start_time}:{self.end_time}\n"
        s += f"Read Mock DataSource: {self.ds.name}\n"
        return s

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class RespectFSTNode(QueryNode):
    """
    Null out all features outside of feature start time

    NOTE: the feature start time is assumed to already be in appropriate units
    for the column: nanoseconds/seconds for anchor time filter, or timestamp
    for timestamp filter
    """

    input_node: NodeRef
    retrieval_time_col: str
    feature_start_time: Union[pendulum.datetime, int]
    features: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return f"Null out any values based on a FeatureStartTime of {self.feature_start_time}"

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()

        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        cond = Field(self.retrieval_time_col) >= to_timestamp(self.feature_start_time)
        project_list = []
        for c in self.columns:
            if c in self.features:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
            else:
                project_list.append(Field(c))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class RespectTTLNode(QueryNode):
    """
    Null out all features with retrieval time > expiration time.
    """

    input_node: NodeRef
    retrieval_time_col: str
    expiration_time_col: str
    features: List[str]

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return f"Null out any values where {self.retrieval_time_col} > {self.expiration_time_col}"

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        cond = Field(self.retrieval_time_col) < Field(self.expiration_time_col)
        project_list = []
        for c in self.input_node.columns:
            if c not in self.features:
                project_list.append(Field(c))
            else:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        return Query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class CustomFilterNode(QueryNode):
    input_node: NodeRef
    filter_str: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    def as_str(self, verbose: bool):
        return f"Apply filter: ({self.filter_str})"

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class TimeFilterNode(QueryNode):
    input_node: NodeRef
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    timestamp_field: str

    def as_str(self, verbose: bool):
        s = ""
        s += f"TimeFilter: {self.start_time}:{self.end_time}\n"
        return s

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        time_field = Field(self.timestamp_field)
        where_conds = []
        if self.start_time is not None:
            where_conds.append(time_field >= to_timestamp(self.start_time))
        if self.end_time is not None:
            where_conds.append(time_field < to_timestamp(self.end_time))
        q = Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        for w in where_conds:
            q = q.where(w)
        return q


@attrs.frozen
class FeatureTimeFilterNode(QueryNode):
    """
    Ensure the data being written by a materialization job to offline/online store only contains
    feature timestamps in the feature_data_time_limits range.
    """

    input_node: NodeRef
    feature_data_time_limits: pendulum.Period
    policy: MaterializationTimeRangePolicy
    timestamp_field: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if self.policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
            policy_str = "Assert time in range:"
        else:
            policy_str = "Apply:"
        return f"{policy_str} TimeFilter: {self.feature_data_time_limits}"

    def _to_query(self) -> pypika.Query:
        if self.policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
            # snowflake/athena are post-fwv4
            raise NotImplementedError
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        time_field = Field(self.timestamp_field)
        where_conds = []
        where_conds.append(time_field >= to_timestamp(self.feature_data_time_limits.start))
        where_conds.append(time_field < to_timestamp(self.feature_data_time_limits.end))
        q = Query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        for w in where_conds:
            q = q.where(w)
        return q


@attrs.frozen
class MetricsCollectorNode(QueryNode):
    """
    Collect metrics on features
    """

    input_node: NodeRef

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return "Collect metrics on features"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError


@attrs.frozen
class AddEffectiveTimestampNode(QueryNode):
    """Augment a dataframe with an effective timestamp.

    The effective timestamp for a given row is the earliest it will be available in the online store for inference.
    For BFVs and BWAFVs, materialization jobs run every `batch_schedule`, so the effective timestamp is calculated as
    window('timestamp_field', batch_schedule).end + data_delay, and is therefore always strictly greater than the
    feature timestamp. For SWAFVs in non-continuous mode, the feature timestamps are aligned to the aggregation window,
    so the effective timestamp is just the feature timestamp. For SFVs, SWAFVs in continuous mode, and feature tables,
    the effective timestamp is also just the feature timestamp.

    Attributes:
        input_node: The input node to be transformed.
        timestamp_field: The column name of the feature timestamp field.
        effective_timestamp_name: The name of the effective timestamp column to be added.
        is_stream: If True, the feature view has a stream data source.
        batch_schedule_seconds: The batch materialization schedule for the feature view, in seconds.
        data_delay_seconds: The data delay for the feature view, in seconds.
        is_temporal_aggregate: If True, the feature view is a WAFV.
    """

    input_node: NodeRef
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int
    is_temporal_aggregate: bool

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + [self.effective_timestamp_name])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        if not verbose:
            return "Add effective timestamp column."

        if self.batch_schedule_seconds == 0 or self.is_stream:
            return f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to the timestamp column '{self.timestamp_field}'."
        else:
            return (
                f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to window('"
                f"{self.timestamp_field}', batch_schedule).end + data_delay where batch_schedule = "
                f"{self.batch_schedule_seconds} seconds and data_delay = {self.data_delay_seconds} seconds."
            )

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = Field(self.timestamp_field)
        else:
            slide_str = f"{self.batch_schedule_seconds} seconds"
            timestamp_col = Field(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 micro
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col -= Interval(microseconds=1)
            effective_timestamp = from_unixtime(
                to_unixtime(timestamp_col)
                - (to_unixtime(timestamp_col) % self.batch_schedule_seconds)
                + self.data_delay_seconds
            )
        return (
            Query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select("*", effective_timestamp.as_(self.effective_timestamp_name))
        )


@attrs.frozen
class AddDurationNode(QueryNode):
    """Adds a duration to a timestamp field"""

    input_node: NodeRef
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return tuple(list(self.input_node.columns) + [self.new_column_name])

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return f"Add {self.duration.in_words()} to {self.timestamp_field} as {self.new_column_name}"

    def _to_query(self) -> pypika.Query:
        input_query = self.input_node._to_query()
        uid = self.input_node.node.__class__.__name__ + "_" + str(id(self.input_node.node))
        return (
            Query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select(
                "*",
                date_add("second", int(self.duration.total_seconds()), Field(self.timestamp_field)).as_(
                    self.new_column_name
                ),
            )
        )


@attrs.frozen
class StreamWatermarkNode(QueryNode):
    input_node: NodeRef
    time_column: str
    stream_watermark: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef, ...]:
        return (self.input_node,)

    def as_str(self, verbose: bool):
        return f"Set Stream Watermark {self.stream_watermark} on the DataFrame"

    def _to_query(self) -> pypika.Query:
        raise NotImplementedError
