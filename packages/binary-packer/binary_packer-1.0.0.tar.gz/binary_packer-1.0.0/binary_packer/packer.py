from struct import Struct
from typing import Any, Generic, Type

from .types import DataClassT, FieldStruct


def build_struct_format(fields_structs: list[tuple[str, FieldStruct[Any, Any]]]) -> str:
    return ''.join(field_struct.fmt for _, field_struct in fields_structs)


class Packer(Generic[DataClassT]):
    """
    Этот класс предполагается приватным, поэтому настоятельно рекомендуется создавать его экземпляры
    исключительно через фабрику PackerFactory. Такой подход гарантирует консистентность пакера.
    """

    def __init__(self, target_cls: Type[DataClassT], fields_structs: list[tuple[str, FieldStruct[Any, Any]]]) -> None:
        self._target_cls = target_cls
        self._fields_structs = fields_structs

        item_schema = build_struct_format(fields_structs)
        self.struct = Struct(item_schema)

    def pack(self, obj: DataClassT) -> bytes:
        return self.struct.pack(
            *[
                getattr(obj, field)
                if struct_info.encoder is None else
                struct_info.encoder(getattr(obj, field))
                for field, struct_info in self._fields_structs
            ]
        )

    def unpack(self, array: bytes) -> DataClassT:
        return self._target_cls(
            **{
                field: value if struct_info.decoder is None else struct_info.decoder(value)
                for (field, struct_info), value in zip(self._fields_structs, self.struct.unpack(array))
            }
        )

    @property
    def size(self) -> int:
        return self.struct.size
