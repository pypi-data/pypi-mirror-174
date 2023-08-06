from typing import Optional

import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql.window import Window

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.common import aggregation_function_pb2
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.time_utils import convert_timestamp_to_epoch


# NOTE: this should _only_ be used by query tree
def construct_full_tafv_df_with_anchor_time(
    fdw: FeatureDefinitionWrapper,
    all_partial_aggregations_df: DataFrame,
    spine_df: Optional[DataFrame],
    respect_feature_start_time: bool,
) -> DataFrame:
    """Computes full aggregates based on partial aggregates.

    The partial aggregates dataframe must have an "_anchor_time" epoch column that represents the start times of tiles.

    If a spine is provided, full aggregates will be computed for the rows in the spine. The spine must also have an
    "_anchor_time" epoch column that contains retrieval epochs. The resulting dataframe will have an "_anchor_time"
    column that represents the start time of the last tile used in the full aggregate.

    If a spine is not provided, full aggregates will be computed with respect to all tiles that exist in the partial
    aggregates dataframe. Again, the resulting dataframe will have a "_anchor_time" column, but for each row it will
    represent the end time (as an epoch) of the last tile used in the full aggregate, instead of the start time.

    For a continuous SWAFV, the "_anchor_time" column does not reflect tiles, so regardless of whether there is a spine
    or not, the resulting dataframe will not modify the "_anchor_time" column at all.

    Note that this method currently does not implement any wildcard behavior.

    Args:
        fdw: The feature view to be aggregated. Must be a WAFV.
        all_partial_aggregations_df: The partial aggregates (i.e. tiles) of the feature view. Must contain a timestamp
            column named "_anchor_time" that represents the start times of the tiles.
        spine_df: If set, represents the spine that the full aggregates should be left-joined against.
        respect_feature_start_time: If True, the computed aggregates will be filtered with respect to the feature view's
            feature start time.

    Returns:
        A dataframe with the full aggregations. For example, if the feature view has a count aggregation with a window of two days, and the partial aggregates dataframe looks like

        +-------+-----------------+-------------------+
        |user_id|count_transaction|       _anchor_time|
        +-------+-----------------+-------------------+
        |      1|                9|2022-05-13 00:00:00|
        |      1|               22|2022-05-14 00:00:00|
        |      1|               43|2022-05-15 00:00:00|
        +-------+-----------------+-------------------+

        and the spine looks like

                    timestamp user_id
        0 2022-10-15 00:00:00       1

        then the resulting full aggregates dataframe would look like

        +-------+-----------------+-------------------+
        |user_id|count_transaction|       _anchor_time|
        +-------+-----------------+-------------------+
        |      1|               65|2022-05-15 00:00:00|
        +-------+-----------------+-------------------+

        Without a spine, the resulting dataframe would look like

        +-------+-----------------------+-------------------+
        |user_id|transaction_count_3d_1d|       _anchor_time|
        +-------+-----------------------+-------------------+
        |      1|                      9|2022-05-14 00:00:00|
        |      1|                     31|2022-05-15 00:00:00|
        |      1|                     65|2022-05-16 00:00:00|
        +-------+-----------------------+-------------------+

        Note that the "_anchor_time" column has been transformed to reflect end times instead of start times. Also note that for simplicity these examples use timestamps instead of epochs, but in reality the columns must be epochs.
    """
    # TODO: drop anchor time concept from full aggregations. Define start & end times of the aggregation window,
    # use the new concepts for joining, and for returning the temporal aggregate feature dataframes

    # TODO: handle wildcards

    spine_join_keys = fdw.join_keys

    if not spine_df:
        # If spine isn't provided, the fake timestamp equals to anchor time + tile_interval, s.t. the output timestamp
        # completely contains the time range of the fully aggregated window. Note, that ideally we would either subtract
        # 1 second from the timestamp, due to tiles having [start, end) format, or convert tiles in (start, end] format.
        # For now, we're not doing 1 due to it being confusing in preview, and not doing 2 due to it requiring more work
        partial_aggregations_df = all_partial_aggregations_df.withColumn(
            TEMPORAL_ANCHOR_COLUMN_NAME,
            functions.col(TEMPORAL_ANCHOR_COLUMN_NAME) + fdw.get_tile_interval_for_version,
        )
    else:
        if not fdw:
            raise ValueError("fdw argument must not be None when spine_df is provided.")

        # TODO: drop anchor column and keep original spine timestamp
        # If spine is provided, round down the time key to the most recent anchor and right join on it + join_keys
        # TODO: ^ see if the above is actually even a good idea because it could hurt our ability to push down filters to the offline store.
        spine_df = spine_df.select(TEMPORAL_ANCHOR_COLUMN_NAME, *spine_join_keys).distinct()

        # Make sure the all join keys & anchor times that occur in spine exist in the partially aggregated df
        # This is necessary in the case when the exact anchor time is missing from partially aggregated df,
        # but the previous tiles belonging to the full aggregation window are available. In this case we shouldn't
        # return null, instead we need to aggregate the existing tiles and return the response.
        # TODO: use union instead of outer join, similar to AsofJoin.
        # TODO: generally refactor this node to look more like AsofJoin, which should lead to performance benefits.
        partial_aggregations_df = all_partial_aggregations_df.join(
            spine_df, on=fdw.join_keys + [TEMPORAL_ANCHOR_COLUMN_NAME], how="outer"
        )

    aggregations = []
    time_aggregation = fdw.trailing_time_window_aggregation
    for feature in time_aggregation.features:
        # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
        # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
        window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
        lower_bound = -(convert_timedelta_for_version(window_duration, fdw.get_feature_store_format_version)) + 1
        window_spec = (
            Window.partitionBy(fdw.join_keys)
            .orderBy(functions.col(TEMPORAL_ANCHOR_COLUMN_NAME).asc())
            .rangeBetween(lower_bound, 0)
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
        if respect_feature_start_time and fdw.feature_start_timestamp:
            unix_feature_start_time = convert_timestamp_to_epoch(
                fdw.feature_start_timestamp, fdw.get_feature_store_format_version
            )
            if fdw.get_tile_interval_for_version != 0:
                aligned_feature_start_time = (
                    unix_feature_start_time - unix_feature_start_time % fdw.get_tile_interval_for_version
                )
            else:
                aligned_feature_start_time = unix_feature_start_time
            # With a spine, the anchor time is a start time; without a spine, the anchor time is an end time.
            aligned_feature_start_anchor_time = aligned_feature_start_time - (
                fdw.get_tile_interval_for_version if spine_df else 0
            )
            filtered_agg = functions.when(
                functions.col(TEMPORAL_ANCHOR_COLUMN_NAME) >= aligned_feature_start_anchor_time,
                agg,
            ).otherwise(functions.lit(None))
        else:
            filtered_agg = agg
        aggregations.append(filtered_agg.alias(feature.output_feature_name))

    output_df = partial_aggregations_df.select(fdw.join_keys + [TEMPORAL_ANCHOR_COLUMN_NAME] + aggregations)

    return output_df
