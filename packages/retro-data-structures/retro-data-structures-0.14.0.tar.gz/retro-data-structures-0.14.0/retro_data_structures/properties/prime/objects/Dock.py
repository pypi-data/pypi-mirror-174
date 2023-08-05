# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Dock(BaseObjectType):
    name: str = dataclasses.field(default='')
    active: bool = dataclasses.field(default=False)
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    dock_index: int = dataclasses.field(default=0)
    area_index: int = dataclasses.field(default=0)
    auto_load: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0xB

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        active = struct.unpack('>?', data.read(1))[0]
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        dock_index = struct.unpack('>l', data.read(4))[0]
        area_index = struct.unpack('>l', data.read(4))[0]
        auto_load = struct.unpack('>?', data.read(1))[0]
        return cls(name, active, position, scale, dock_index, area_index, auto_load)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x07')  # 7 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.active))
        self.position.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>l', self.dock_index))
        data.write(struct.pack('>l', self.area_index))
        data.write(struct.pack('>?', self.auto_load))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            active=data['active'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            dock_index=data['dock_index'],
            area_index=data['area_index'],
            auto_load=data['auto_load'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'active': self.active,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'dock_index': self.dock_index,
            'area_index': self.area_index,
            'auto_load': self.auto_load,
        }
