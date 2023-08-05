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
class WarWasp(BaseObjectType):
    name: str = dataclasses.field(default='')
    patterned_flavor_type: int = dataclasses.field(default=0)
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000005: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000006: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    collider: bool = dataclasses.field(default=False)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    unknown_3: AssetId = dataclasses.field(default=0x0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x21

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        patterned_flavor_type = struct.unpack('>l', data.read(4))[0]
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000005 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000006 = ActorParameters.from_stream(data, property_size)
        collider = struct.unpack('>?', data.read(1))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        wpsc = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        particle = struct.unpack(">L", data.read(4))[0]
        unknown_3 = struct.unpack(">L", data.read(4))[0]
        return cls(name, patterned_flavor_type, position, rotation, scale, unnamed_0x00000005, unnamed_0x00000006, collider, damage_info_1, wpsc, damage_info_2, particle, unknown_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\r')  # 13 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>l', self.patterned_flavor_type))
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)
        data.write(struct.pack('>?', self.collider))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack(">L", self.wpsc))
        self.damage_info_2.to_stream(data)
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack(">L", self.unknown_3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            patterned_flavor_type=data['patterned_flavor_type'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000005=PatternedAITypedef.from_json(data['unnamed_0x00000005']),
            unnamed_0x00000006=ActorParameters.from_json(data['unnamed_0x00000006']),
            collider=data['collider'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            wpsc=data['wpsc'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            particle=data['particle'],
            unknown_3=data['unknown_3'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'patterned_flavor_type': self.patterned_flavor_type,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'collider': self.collider,
            'damage_info_1': self.damage_info_1.to_json(),
            'wpsc': self.wpsc,
            'damage_info_2': self.damage_info_2.to_json(),
            'particle': self.particle,
            'unknown_3': self.unknown_3,
        }
