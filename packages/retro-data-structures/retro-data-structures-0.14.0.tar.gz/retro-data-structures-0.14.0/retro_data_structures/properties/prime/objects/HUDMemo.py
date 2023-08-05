# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.AssetId import AssetId


@dataclasses.dataclass()
class HUDMemo(BaseObjectType):
    name: str = dataclasses.field(default='')
    first_message_timer: float = dataclasses.field(default=0.0)
    unknown_1: bool = dataclasses.field(default=False)
    memo_type: int = dataclasses.field(default=0)  # Choice
    strg: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffff)
    active: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x17

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        first_message_timer = struct.unpack('>f', data.read(4))[0]
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        memo_type = struct.unpack(">L", data.read(4))[0]
        strg = struct.unpack(">L", data.read(4))[0]
        active = struct.unpack('>?', data.read(1))[0]
        return cls(name, first_message_timer, unknown_1, memo_type, strg, active)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x06')  # 6 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>f', self.first_message_timer))
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack(">L", self.memo_type))
        data.write(struct.pack(">L", self.strg))
        data.write(struct.pack('>?', self.active))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            first_message_timer=data['first_message_timer'],
            unknown_1=data['unknown_1'],
            memo_type=data['memo_type'],
            strg=data['strg'],
            active=data['active'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'first_message_timer': self.first_message_timer,
            'unknown_1': self.unknown_1,
            'memo_type': self.memo_type,
            'strg': self.strg,
            'active': self.active,
        }
