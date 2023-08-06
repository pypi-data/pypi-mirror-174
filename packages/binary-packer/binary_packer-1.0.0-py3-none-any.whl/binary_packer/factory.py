
from typing import Any, Generic, Iterable, Type

from .packer import Packer
from .types import DataClassT, FieldStruct


class PackerFactory(Generic[DataClassT]):
    def __init__(self, target_cls: Type[DataClassT], **fields_structs: FieldStruct[Any, Any]) -> None:
        self._target_cls = target_cls
        self._check_fields_exist_in_target_cls(fields_structs.keys())

        self._fields_structs = fields_structs

    def make_packer(self, *fields: str) -> Packer[DataClassT]:
        self._check_required_fields_exist_in_fields_structs(fields)

        fields_structs = [
            (field, struct_info) for field, struct_info in self._fields_structs.items() if field in fields
        ]
        return Packer(target_cls=self._target_cls, fields_structs=fields_structs)

    def _check_fields_exist_in_target_cls(self, fields: Iterable[str]) -> None:
        cls_fields = getattr(self._target_cls, '__dataclass_fields__', {})  # type: dict[str, Any]
        for field in fields:
            if field not in cls_fields:
                raise ValueError(f'Field <{field}> does not exist in target class <{self._target_cls.__name__}>')

    def _check_required_fields_exist_in_fields_structs(self, fields: Iterable[str]) -> None:
        for field in fields:
            if field not in self._fields_structs:
                raise ValueError(f'There is no struct for field <{field}> in packer factory')
