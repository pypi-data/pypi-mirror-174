
# BINARY PACKER #

Light and fast packer python dataclasses to bytes

[![Build Status](https://app.travis-ci.com/moff4/packer.svg?branch=master)](https://app.travis-ci.com/moff4/packer)
[![CodeFactor](https://www.codefactor.io/repository/github/moff4/packer/badge)](https://www.codefactor.io/repository/github/moff4/packer)


## Install


## How it works

It's a wrap! A wrap over stdlib [struct](https://docs.python.org/3/library/struct.html)  
So it converts values into bytes using `struct.pack()`.  
But it does not save keys and values' types in bytes, so be sure about how you configure packer for packing and unpacking. 

## Why and when should it be used?

We all like to use json/xml/pickle and other popular libraries for dumping data, but sometimes they are too slow or result's size ot too large.  
This library works much faster than other packers like json and makes result a lot more compact.

## Example of Usage

```python
import uuid
from typing import Optional
from dataclasses import dataclass

from binary_packer import PackerFactory, FieldStruct


@dataclass
class Person:
    id: uuid.UUID
    name: Optional[str] = None  # max length is 20 bytes
    age: Optional[int] = None

person = Person(id=uuid.uuid4(), name='vaschevsky', age=33)


factory = PackerFactory(
    Person,
    id=FieldStruct[uuid.UUID, bytes](
        '16s',  # '16s' is for bytearray length of 16, uuid as bytearray also 16 bytes
        encoder=lambda uid: uid.bytes,
        decoder=lambda uid_as_bytes: uuid.UUID(bytes=uid_as_bytes),
    ),
    name=FieldStruct[str, bytes](
        '20s',  # '20s' is for bytearray length of 20, each byte is ascii char
        encoder=lambda name: name.encode(),
        decoder=lambda name_as_bytes: name_as_bytes.decode().strip('\x00'),
    ),
    age=FieldStruct[int, int](
        'B',  #  'B' is for unsigned tiny int (1 byte) => age can be any value from 0 to 255,
        # no need for custom encoder/decoder
    )
)

packer_1 = factory.make_packer('id', 'name', 'age')
packer_2 = factory.make_packer('id', 'name')
packer_3 = factory.make_packer('id')

for packer in (packer_1, packer_2, packer_3):
    data_as_bytes = packer.pack(person)
    print(f'{len(data_as_bytes)=}')
    unpacked_person = packer.unpack(data_as_bytes)
    print(f'{unpacked_person=}')

# will be printed:
# len(data_as_bytes)=37
# unpacked_person=Person(id=UUID('a72decb7-7f9e-497b-ac91-692e316a7580'), name='vaschevsky', age=33)
# len(data_as_bytes)=36
# unpacked_person=Person(id=UUID('a72decb7-7f9e-497b-ac91-692e316a7580'), name='vaschevsky', age=None)
# len(data_as_bytes)=16
# unpacked_person=Person(id=UUID('a72decb7-7f9e-497b-ac91-692e316a7580'), name=None, age=None)
```


[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/komissarov)

