from typeguard import typechecked

from tecton_core import id_helper
from tecton_core.specs import utils
from tecton_proto.args import new_transformation_pb2 as new_transformation__args_pb2
from tecton_proto.args import user_defined_function_pb2
from tecton_proto.data import new_transformation_pb2 as new_transformation__data_pb2

__all__ = [
    "TransformationSpec",
]


@utils.frozen_strict
class TransformationSpec:
    name: str
    id: str
    transformation_mode: new_transformation__args_pb2.TransformationMode
    user_function: user_defined_function_pb2.UserDefinedFunction

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: new_transformation__data_pb2.NewTransformation) -> "TransformationSpec":
        return cls(
            name=proto.fco_metadata.name,
            id=id_helper.IdHelper.to_string(proto.transformation_id),
            transformation_mode=proto.transformation_mode,
            user_function=utils.get_field_or_none(proto, "user_function"),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: new_transformation__args_pb2.NewTransformationArgs) -> "TransformationSpec":
        return cls(
            name=proto.info.name,
            id=id_helper.IdHelper.to_string(proto.transformation_id),
            transformation_mode=proto.transformation_mode,
            user_function=utils.get_field_or_none(proto, "user_function"),
        )
