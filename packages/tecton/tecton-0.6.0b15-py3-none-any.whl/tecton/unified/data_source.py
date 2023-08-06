from __future__ import annotations

import datetime
from typing import Dict
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton import conf
from tecton import declarative
from tecton._internals import display
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton.interactive import data_frame
from tecton.interactive import snowflake_api
from tecton.interactive import spark_api
from tecton.unified import common as unified_common
from tecton.unified import utils as unified_utils
from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import framework_version_pb2
from tecton_proto.data import virtual_data_source_pb2 as virtual_data_source__data_pb2
from tecton_proto.metadataservice import metadata_service_pb2

BatchConfigType = Union[
    declarative.FileConfig,
    declarative.HiveConfig,
    declarative.RedshiftConfig,
    declarative.SnowflakeConfig,
    declarative.data_source.SparkBatchConfig,
]

StreamConfigType = Union[declarative.KinesisConfig, declarative.KafkaConfig, declarative.data_source.SparkStreamConfig]


@attrs.define
class DataSource(unified_common.BaseTectonObject):
    """Base class for Data Source classes.

    Attributes:
        _spec: A data source spec, i.e. a dataclass representation of the Tecton object that is used in most functional
            use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
            applied objects fetched from the backend, are assumed valid.
        _args: A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
            and fetched from the Tecton backend.
        _args_supplement: A supplement to the _args proto that is needed to create the Data Source spec.
    """

    _spec: Optional[specs.DataSourceSpec] = attrs.field(repr=False)
    _args: Optional[virtual_data_source__args_pb2.VirtualDataSourceArgs] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )
    _args_supplement: Optional[specs.DataSourceSpecArgsSupplement] = attrs.field(
        repr=False, on_setattr=attrs.setters.frozen
    )

    @property
    def _is_valid(self):
        return self._spec is not None

    @sdk_decorators.sdk_public_method
    def validate(self) -> None:
        if self._is_valid:
            # Already valid.
            return

        # TODO add validation
        self._spec = specs.DataSourceSpec.from_args_proto(self._args, self._args_supplement)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this data source."""
        request = metadata_service_pb2.GetVirtualDataSourceSummaryRequest()
        request.fco_locator.id.CopyFrom(id_helper.IdHelper.from_string(self._spec.id))
        request.fco_locator.workspace = self._spec.workspace

        response = metadata_service.instance().GetVirtualDataSourceSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.sdk_public_method
    @unified_utils.requires_validation
    def get_dataframe(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        *,
        apply_translator: bool = True,
    ) -> data_frame.TectonDataFrame:
        if conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
            return snowflake_api.get_dataframe_for_data_source(self._spec, start_time, end_time)
        else:
            return spark_api.get_dataframe_for_data_source(self._spec, start_time, end_time, apply_translator)


@attrs.define
class BatchSource(DataSource):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        batch_config: BatchConfigType,
    ):
        from tecton.cli import common as cli_common

        source_info = cli_common.get_fco_source_info()

        ds_args = _build_base_data_source_args(name, description, tags, owner)
        ds_args.type = data_source_type_pb2.DataSourceType.BATCH
        batch_config._merge_batch_args(ds_args)

        info = unified_common.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, None),
        )

    @classmethod
    @typechecked
    def _create_from_data_proto(cls, proto: virtual_data_source__data_pb2.VirtualDataSource) -> BatchSource:
        """Create a BatchSource from a data proto."""
        spec = specs.DataSourceSpec.from_data_proto(proto)
        info = unified_common.TectonObjectInfo.from_data_proto(proto.fco_metadata, proto.virtual_data_source_id)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None, args_supplement=None)
        return obj


@attrs.define
class StreamSource(DataSource):
    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        batch_config: BatchConfigType,
        stream_config: StreamConfigType,
    ):
        from tecton.cli import common as cli_common

        source_info = cli_common.get_fco_source_info()

        ds_args = _build_base_data_source_args(name, description, tags, owner)
        ds_args.type = data_source_type_pb2.DataSourceType.STREAM_WITH_BATCH
        batch_config._merge_batch_args(ds_args)
        stream_config._merge_stream_args(ds_args)
        info = unified_common.TectonObjectInfo.from_args_proto(ds_args.info, ds_args.virtual_data_source_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=ds_args,
            source_info=source_info,
            args_supplement=_build_args_supplement(batch_config, stream_config),
        )

    @classmethod
    @typechecked
    def _create_from_data_proto(cls, proto: virtual_data_source__data_pb2.VirtualDataSource) -> StreamSource:
        """Create a StreamSource from a data proto."""
        spec = specs.DataSourceSpec.from_data_proto(proto)
        info = unified_common.TectonObjectInfo.from_data_proto(proto.fco_metadata, proto.virtual_data_source_id)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None, args_supplement=None)
        return obj


def _build_base_data_source_args(
    name: str, description: Optional[str], tags: Optional[Dict[str, str]], owner: Optional[str]
):
    return virtual_data_source__args_pb2.VirtualDataSourceArgs(
        virtual_data_source_id=id_helper.IdHelper.generate_id(),
        info=basic_info_pb2.BasicInfo(
            name=name,
            description=description,
            tags=tags,
            owner=owner,
        ),
        version=framework_version_pb2.FrameworkVersion.FWV5,
    )


def _build_args_supplement(
    batch_config: BatchConfigType, stream_config: Optional[StreamConfigType]
) -> specs.DataSourceSpecArgsSupplement:
    supplement = specs.DataSourceSpecArgsSupplement()
    if isinstance(
        batch_config,
        (declarative.FileConfig, declarative.HiveConfig, declarative.RedshiftConfig, declarative.SnowflakeConfig),
    ):
        supplement.batch_post_processor = batch_config.post_processor
    elif isinstance(batch_config, declarative.data_source.SparkBatchConfig):
        supplement.batch_data_source_function = batch_config.data_source_function
    else:
        raise TypeError(f"Unexpected batch_config type: {batch_config}")

    if isinstance(stream_config, (declarative.KinesisConfig, declarative.KafkaConfig)):
        supplement.stream_post_processor = stream_config.post_processor
    elif isinstance(stream_config, declarative.data_source.SparkStreamConfig):
        supplement.stream_data_source_function = stream_config.data_source_function
    elif stream_config is not None:
        raise TypeError(f"Unexpected stream_config type: {stream_config}")

    return supplement
