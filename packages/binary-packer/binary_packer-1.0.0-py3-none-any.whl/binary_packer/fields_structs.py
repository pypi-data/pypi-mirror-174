
from uuid import UUID

from .types import FieldStruct

INT_SIZE_SIGN_FORMAT_MAP = {
    (1, True): 'b',
    (1, False): 'B',
    (2, True): 'h',
    (2, False): 'H',
    (4, True): 'l',
    (4, False): 'L',
    (8, True): 'q',
    (8, False): 'Q',
}

FLOAT_SIZE_FORMAT_MAP = {
    2: 'e',
    4: 'f',
    8: 'd',
}


def uuid_field_struct() -> FieldStruct[UUID, bytes]:
    return FieldStruct[UUID, bytes](
        '16s',  # '16s' is for bytearray length of 16, uuid as bytearray also 16 bytes
        encoder=lambda uid: uid.bytes,
        decoder=lambda uid_as_bytes: UUID(bytes=uid_as_bytes),
    )


def bytes_field_struct(max_len: int) -> FieldStruct[bytes, bytes]:
    """
        be careful using this formatter, after unpack here can apper zero-bytes at the end
    """
    return FieldStruct[bytes, bytes](f'{max_len}s')


def str_field_struct(max_len: int) -> FieldStruct[str, bytes]:
    """
        max_len - maximum possible length of string as bytes (usually depends on encoding)
    """
    return FieldStruct[str, bytes](
        f'{max_len}s',
        encoder=lambda name: name.encode(),
        decoder=lambda name_as_bytes: name_as_bytes.decode().strip('\x00'),
    )


def int_field_struct(size_in_bytes: int, signed: bool = True) -> FieldStruct[int, int]:
    if not 1 <= size_in_bytes <= 8:
        raise ValueError('invalid value for size_in_bytes, it can be 1-8')

    if size_in_bytes == 3:
        size_in_bytes = 4
    elif size_in_bytes in {5, 6, 7}:
        size_in_bytes = 8

    return FieldStruct(INT_SIZE_SIGN_FORMAT_MAP[(size_in_bytes, signed)])


def bool_field_struct() -> FieldStruct[bool, int]:
    return FieldStruct('?', encoder=int, decoder=bool)


def float_field_struct(size_in_bytes: int) -> FieldStruct[float, float]:
    """
        be careful choosing size_in_bytes, as it can change precision
    """

    if not 1 <= size_in_bytes <= 8:
        raise ValueError('invalid value for size_in_bytes, it can be 1-8')

    if size_in_bytes == 1:
        size_in_bytes = 2
    elif size_in_bytes == 3:
        size_in_bytes = 4
    elif size_in_bytes in {5, 6, 7}:
        size_in_bytes = 8

    return FieldStruct[float, float](FLOAT_SIZE_FORMAT_MAP[size_in_bytes])
