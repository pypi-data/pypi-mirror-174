# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.LayerSwitch import LayerSwitch
from retro_data_structures.properties.prime.core.AssetId import AssetId
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class SpecialFunction(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    function: int = dataclasses.field(default=0)  # Choice
    unknown_1: str = dataclasses.field(default='')
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unnamed_0x00000008: LayerSwitch = dataclasses.field(default_factory=LayerSwitch)
    unnamed_0x00000009: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    active: bool = dataclasses.field(default=False)
    unknown_5: float = dataclasses.field(default=0.0)
    used_by_spinner_controller_1: AssetId = dataclasses.field(default=0x0)
    used_by_spinner_controller_2: AssetId = dataclasses.field(default=0x0)
    used_by_spinner_controller_3: AssetId = dataclasses.field(default=0x0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x3A

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        function = struct.unpack(">L", data.read(4))[0]
        unknown_1 = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000008 = LayerSwitch.from_stream(data, property_size)
        unnamed_0x00000009 = enums.PlayerItem.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        used_by_spinner_controller_1 = struct.unpack(">L", data.read(4))[0]
        used_by_spinner_controller_2 = struct.unpack(">L", data.read(4))[0]
        used_by_spinner_controller_3 = struct.unpack(">L", data.read(4))[0]
        return cls(name, position, rotation, function, unknown_1, unknown_2, unknown_3, unknown_4, unnamed_0x00000008, unnamed_0x00000009, active, unknown_5, used_by_spinner_controller_1, used_by_spinner_controller_2, used_by_spinner_controller_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0f')  # 15 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack(">L", self.function))
        data.write(self.unknown_1.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        self.unnamed_0x00000008.to_stream(data)
        self.unnamed_0x00000009.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack(">L", self.used_by_spinner_controller_1))
        data.write(struct.pack(">L", self.used_by_spinner_controller_2))
        data.write(struct.pack(">L", self.used_by_spinner_controller_3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            function=data['function'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unnamed_0x00000008=LayerSwitch.from_json(data['unnamed_0x00000008']),
            unnamed_0x00000009=enums.PlayerItem.from_json(data['unnamed_0x00000009']),
            active=data['active'],
            unknown_5=data['unknown_5'],
            used_by_spinner_controller_1=data['used_by_spinner_controller_1'],
            used_by_spinner_controller_2=data['used_by_spinner_controller_2'],
            used_by_spinner_controller_3=data['used_by_spinner_controller_3'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'function': self.function,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'active': self.active,
            'unknown_5': self.unknown_5,
            'used_by_spinner_controller_1': self.used_by_spinner_controller_1,
            'used_by_spinner_controller_2': self.used_by_spinner_controller_2,
            'used_by_spinner_controller_3': self.used_by_spinner_controller_3,
        }
