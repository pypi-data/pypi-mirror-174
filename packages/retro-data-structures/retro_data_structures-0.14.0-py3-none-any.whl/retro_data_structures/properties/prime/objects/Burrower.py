# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Burrower(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    unnamed_0x00000009: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    always_ffffffff: int = dataclasses.field(default=0)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x7F

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000004 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000005 = ActorParameters.from_stream(data, property_size)
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        wpsc = struct.unpack(">L", data.read(4))[0]
        unnamed_0x00000009 = DamageInfo.from_stream(data, property_size)
        particle_3 = struct.unpack(">L", data.read(4))[0]
        always_ffffffff = struct.unpack('>l', data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, particle_1, particle_2, wpsc, unnamed_0x00000009, particle_3, always_ffffffff, particle_4)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\r')  # 13 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.wpsc))
        self.unnamed_0x00000009.to_stream(data)
        data.write(struct.pack(">L", self.particle_3))
        data.write(struct.pack('>l', self.always_ffffffff))
        data.write(struct.pack(">L", self.particle_4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            wpsc=data['wpsc'],
            unnamed_0x00000009=DamageInfo.from_json(data['unnamed_0x00000009']),
            particle_3=data['particle_3'],
            always_ffffffff=data['always_ffffffff'],
            particle_4=data['particle_4'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'wpsc': self.wpsc,
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'particle_3': self.particle_3,
            'always_ffffffff': self.always_ffffffff,
            'particle_4': self.particle_4,
        }
