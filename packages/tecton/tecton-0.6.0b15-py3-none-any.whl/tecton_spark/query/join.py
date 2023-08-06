from typing import List
from typing import Optional

import attrs
import pendulum
import pyspark
import pyspark.sql.functions as F
import pyspark.sql.window as spark_window
from pyspark.sql import functions
from pyspark.sql.window import Window

from tecton_core import conf
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.logger import get_logger
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.common import aggregation_function_pb2
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.materialization_params import MaterializationParams
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.query.node import SparkExecNode
from tecton_spark.time_utils import convert_timestamp_to_epoch


logger = get_logger("query_tree")
ASOF_JOIN_TIMESTAMP_COL_1 = "_asof_join_timestamp_1"
ASOF_JOIN_TIMESTAMP_COL_2 = "_asof_join_timestamp_2"


@attrs.frozen
class JoinSparkNode(SparkExecNode):
    """
    A basic left join on 2 inputs
    """

    left: SparkExecNode
    right: SparkExecNode
    join_cols: List[str]
    how: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)
        return left_df.join(right_df, how=self.how, on=self.join_cols)


@attrs.frozen
class AsofJoinInputSparkContainer:
    node: SparkExecNode
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str]
    prefix: Optional[str]


@attrs.frozen
class AsofJoinSparkNode(SparkExecNode):
    """
    A "basic" asof join on 2 inputs.
    LEFT asof_join RIGHT has the following behavior:
        For each row on the left side, find the latest (but <= in time) matching (by join key) row on the right side, and associate the right side's columns to that row.
    The result is a dataframe with the same number of rows as LEFT, with additional columns. These additional columns are prefixed with f"{right_prefix}_". This is the built-in behavior of the tempo library.

    There are a few ways this behavior can be implemented, but by test the best performing method has been to union the two inputs and use a "last" window function with skip_nulls.
    In order to match the rows together.
    """

    left_container: AsofJoinInputSparkContainer
    right_container: AsofJoinInputSparkContainer
    join_cols: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left_container.node.to_dataframe(spark)
        right_df = self.right_container.node.to_dataframe(spark)
        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp < spine timestamp.
        # The ASOF_JOIN_TIMESTAMP_COL_1 and ASOF_JOIN_TIMESTAMP_COL_2 columns will be used for sorting.
        left_df = left_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_1, F.col(self.left_container.timestamp_field))
        left_df = left_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_2, F.col(self.left_container.timestamp_field))
        right_df = right_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_1, F.col(self.right_container.effective_timestamp_field))
        right_df = right_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_2, F.col(self.right_container.timestamp_field))

        if conf.get_bool("ENABLE_TEMPO"):
            from tempo import TSDF

            # TODO: Tempo needs to asof join using 2 columns.
            logger.warning("Do not use Tempo for ASOF join. It has not been validated.")

            # We'd like to do the following:
            left_tsdf = TSDF(left_df, ts_col=ASOF_JOIN_TIMESTAMP_COL_1, partition_cols=self.join_cols)
            right_tsdf = TSDF(right_df, ts_col=ASOF_JOIN_TIMESTAMP_COL_1, partition_cols=self.join_cols)
            # TODO(TEC-9494) - we could speed up by setting partition_ts to ttl size
            out = left_tsdf.asofJoin(right_tsdf, right_prefix=self.right_container.prefix, skipNulls=False).df
            return out
        else:
            # includes both fv join keys and the temporal asof join key
            timestamp_join_cols = [ASOF_JOIN_TIMESTAMP_COL_1, ASOF_JOIN_TIMESTAMP_COL_2]
            common_cols = self.join_cols + timestamp_join_cols
            left_nonjoin_cols = list(set(left_df.columns) - set(common_cols))
            # we additionally include the right time field though we join on the left's time field.
            # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
            right_nonjoin_cols = list(set(right_df.columns) - set(self.join_cols + timestamp_join_cols))

            right_struct_col_name = "_right_values_struct"
            # wrap fields on the right in a struct. This is to work around null feature values and ignorenulls
            # used during joining/window function.
            cols_to_wrap = [F.col(c).alias(f"{self.right_container.prefix}_{c}") for c in right_nonjoin_cols]
            right_df = right_df.withColumn(right_struct_col_name, F.struct(*cols_to_wrap))
            # schemas have to match exactly so that the 2 dataframes can be unioned together.
            right_struct_schema = right_df.schema[right_struct_col_name].dataType
            left_full_cols = (
                [F.lit(True).alias("is_left")]
                + [F.col(x) for x in common_cols]
                + [F.col(x) for x in left_nonjoin_cols]
                + [F.lit(None).alias(right_struct_col_name).cast(right_struct_schema)]
            )
            right_full_cols = (
                [F.lit(False).alias("is_left")]
                + [F.col(x) for x in common_cols]
                + [F.lit(None).alias(x) for x in left_nonjoin_cols]
                + [F.col(right_struct_col_name)]
            )
            left_df = left_df.select(left_full_cols)
            right_df = right_df.select(right_full_cols)
            union = left_df.union(right_df)
            window_spec = (
                spark_window.Window.partitionBy(self.join_cols)
                .orderBy([F.col(c).cast("long").asc() for c in timestamp_join_cols])
                .rangeBetween(spark_window.Window.unboundedPreceding, spark_window.Window.currentRow)
            )
            right_window_funcs = [
                F.last(F.col(right_struct_col_name), ignorenulls=True).over(window_spec).alias(right_struct_col_name)
            ]
            # We use the right side of asof join to find the latest values to augment to the rows from the left side.
            # Then, we drop the right side's rows.
            spine_with_features_df = union.select(common_cols + left_nonjoin_cols + right_window_funcs).filter(
                f"is_left"
            )
            # unwrap the struct to return the fields
            return spine_with_features_df.select(self.join_cols + left_nonjoin_cols + [f"{right_struct_col_name}.*"])


@attrs.frozen
class AsofJoinFullAggSparkNode(SparkExecNode):
    """
    An asof join very similar to AsofJoinNode, but with a change where it does
    the full aggregation rollup (rather than a last).

    NOTE: This should only be used for window aggregates.

    TODO: reuse code across FullAggNode and AsofJoinNode and this one.

    LEFT asof_join RIGHT has the following behavior:
        For each row in the spine, find the matching partial aggregates (by time range)
        and run the appropriate full aggregate over those rows.

    The result is a dataframe with the same number of rows as the spine, with
    additional columns of the fully aggregated features (or null).

    There are a few ways this behavior can be implemented, but by test the best
    performing method has been to union the two inputs and use a window
    function for the aggregates.
    """

    spine: SparkExecNode
    partial_agg_node: SparkExecNode
    fdw: FeatureDefinitionWrapper

    def _get_aggregations(self):
        time_aggregation = self.fdw.trailing_time_window_aggregation
        feature_store_format_version = self.fdw.get_feature_store_format_version
        aggregations = []
        for feature in time_aggregation.features:
            # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
            # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
            window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
            earliest_anchor_time = -(convert_timedelta_for_version(window_duration, feature_store_format_version)) + 1
            window_spec = (
                Window.partitionBy(self.fdw.join_keys)
                .orderBy(functions.col(TEMPORAL_ANCHOR_COLUMN_NAME).asc())
                .rangeBetween(earliest_anchor_time, 0)
            )
            aggregation_plan = get_aggregation_plan(
                feature.function, feature.function_params, time_aggregation.is_continuous, time_aggregation.time_key
            )
            names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            input_columns = [functions.col(name) for name in names]

            if feature.function == aggregation_function_pb2.AGGREGATION_FUNCTION_LAST_DISTINCT_N:
                # There isn't an Scala Encoder that works with a list directly, so instead we wrap the list in an object. Here we
                # strip the object to get just the list.
                agg = aggregation_plan.full_aggregation_transform(names[0], window_spec).values
            else:
                agg = aggregation_plan.full_aggregation_transform(input_columns, window_spec)

            # respect feature start time by nulling out any aggregates before it
            # TODO: handle somewhere else?
            if self.fdw.feature_start_timestamp:
                materialization_params = MaterializationParams.from_feature_definition(self.fdw)
                unix_feature_start_time = convert_timestamp_to_epoch(
                    self.fdw.feature_start_timestamp, feature_store_format_version
                )
                if self.fdw.get_tile_interval_for_version != 0:
                    aligned_feature_start_time = (
                        unix_feature_start_time - unix_feature_start_time % self.fdw.get_tile_interval_for_version
                    )
                else:
                    aligned_feature_start_time = unix_feature_start_time
                # anchor time for wafv is on the left side of the interval
                aligned_feature_start_anchor_time = aligned_feature_start_time - self.fdw.get_tile_interval_for_version
                filtered_agg = functions.when(
                    functions.col(TEMPORAL_ANCHOR_COLUMN_NAME) >= aligned_feature_start_anchor_time,
                    agg,
                ).otherwise(functions.lit(None))
            else:
                filtered_agg = agg

            aggregations.append(filtered_agg.alias(feature.output_feature_name))
        return aggregations

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.spine.to_dataframe(spark)
        right_df = self.partial_agg_node.to_dataframe(spark)

        join_keys = self.fdw.join_keys

        # includes both fv join keys and the temporal asof join key
        # TODO: do this better
        timestamp_join_cols = ["_anchor_time"]
        common_cols = join_keys + timestamp_join_cols
        left_nonjoin_cols = list(set(left_df.columns) - set(common_cols))
        left_prefix = "_tecton_left"
        left_prefixed_nonjoin_cols = [f"{left_prefix}_{x}" for x in left_nonjoin_cols]
        right_nonjoin_cols = list(set(right_df.columns) - set(join_keys + timestamp_join_cols))

        left_full_cols = (
            [F.lit(True).alias("is_left")]
            + [F.col(x) for x in common_cols]
            + [F.col(x).alias(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [F.lit(None).alias(x) for x in right_nonjoin_cols]
        )
        right_full_cols = (
            [F.lit(False).alias("is_left")]
            + [F.col(x) for x in common_cols]
            + [F.lit(None).alias(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [F.col(x) for x in right_nonjoin_cols]
        )
        left_df = left_df.select(left_full_cols)
        right_df = right_df.select(right_full_cols)
        union = left_df.union(right_df)

        aggregations = self._get_aggregations()

        output_columns = common_cols + [F.col(f"{left_prefix}_{x}").alias(x) for x in left_nonjoin_cols] + aggregations
        output_df = union.select(output_columns).filter("is_left")

        return output_df
