import tempfile
from datetime import datetime
from typing import Dict
from typing import Optional

from pyspark import sql as pyspark_sql
from pyspark.sql import streaming as pyspark_streaming

from tecton import conf
from tecton import tecton_context
from tecton._internals import errors
from tecton.interactive.data_frame import TectonDataFrame
from tecton.tecton_context import TectonContext
from tecton_core import specs
from tecton_core.query import builder
from tecton_core.query import nodes
from tecton_spark import data_source_helper


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: datetime,
    end_time: datetime,
    apply_translator: bool,
) -> TectonDataFrame:
    if conf.get_bool("QUERYTREE_ENABLED"):
        return get_dataframe_for_data_source_query_tree(data_source, start_time, end_time, apply_translator)
    else:
        return get_dataframe_for_data_source_legacy(data_source, start_time, end_time, apply_translator)


def get_dataframe_for_data_source_legacy(
    data_source: specs.DataSourceSpec,
    start_time: datetime,
    end_time: datetime,
    apply_translator: bool,
) -> TectonDataFrame:
    spark = TectonContext.get_instance()._spark
    if isinstance(data_source.batch_source, specs.SparkBatchSourceSpec):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        df = data_source_helper.get_ds_dataframe(
            spark,
            data_source=data_source,
            consume_streaming_data_source=False,
            start_time=start_time,
            end_time=end_time,
        )
        return TectonDataFrame._create(df)
    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        df = data_source_helper.get_ds_dataframe(
            spark,
            data_source=data_source,
            consume_streaming_data_source=False,
            start_time=start_time,
            end_time=end_time,
        )
        return TectonDataFrame._create(df)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        df = data_source_helper.get_non_dsf_raw_dataframe(spark, data_source.batch_source)
        return TectonDataFrame._create(df)


def get_dataframe_for_data_source_query_tree(
    data_source: specs.DataSourceSpec,
    start_time: datetime,
    end_time: datetime,
    apply_translator: bool,
) -> TectonDataFrame:
    spark = TectonContext.get_instance()._spark
    if isinstance(data_source.batch_source, specs.SparkBatchSourceSpec):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)

    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        node = nodes.RawDataSourceScanNode(data_source).as_ref()
        return TectonDataFrame._create(node)


def start_stream_preview(
    data_source: specs.DataSourceSpec,
    table_name: str,
    apply_translator: bool,
    option_overrides: Optional[Dict[str, str]],
) -> pyspark_streaming.StreamingQuery:
    df = get_stream_preview_dataframe(data_source, apply_translator, option_overrides)

    with tempfile.TemporaryDirectory() as d:
        return (
            df.writeStream.format("memory")
            .queryName(table_name)
            .option("checkpointLocation", d)
            .outputMode("append")
            .start()
        )


def get_stream_preview_dataframe(
    data_source: specs.DataSourceSpec, apply_translator: bool, option_overrides: Optional[Dict[str, str]]
) -> pyspark_sql.DataFrame:
    """
    Helper function that allows start_stream_preview() to be unit tested, since we can't easily unit test writing
    to temporary tables.
    """
    spark = tecton_context.TectonContext.get_instance()._spark

    if apply_translator or isinstance(data_source.stream_source, specs.SparkStreamSourceSpec):
        return data_source_helper.get_ds_dataframe(
            spark, data_source, consume_streaming_data_source=True, stream_option_overrides=option_overrides
        )
    else:
        return data_source_helper.get_non_dsf_raw_stream_dataframe(spark, data_source.stream_source, option_overrides)
