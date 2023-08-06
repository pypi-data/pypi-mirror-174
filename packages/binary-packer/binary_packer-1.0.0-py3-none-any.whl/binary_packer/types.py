
from typing import Callable, Generic, Optional, TypeVar

DataClassT = TypeVar('DataClassT')
FieldTypeT = TypeVar('FieldTypeT')
StructTypeT = TypeVar('StructTypeT', bytes, float, int, bool)


class FieldStruct(Generic[FieldTypeT, StructTypeT]):
    def __init__(
        self,
        fmt: str,
        encoder: Optional[Callable[[FieldTypeT], StructTypeT]] = None,
        decoder: Optional[Callable[[StructTypeT], FieldTypeT]] = None,
    ) -> None:
        self.fmt = fmt
        self.encoder = encoder  # type: Optional[Callable[[FieldTypeT], StructTypeT]]
        self.decoder = decoder  # type: Optional[Callable[[StructTypeT], FieldTypeT]]
