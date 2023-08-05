# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Thardus(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: bool = dataclasses.field(default=False)
    rock_weak_point_1_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_2_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_3_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_4_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_5_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_6_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    rock_weak_point_7_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_1_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_2_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_3_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_4_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_5_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_6_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_weak_point_7_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    state_machine: AssetId = dataclasses.field(metadata={'asset_types': ['AFSM']}, default=0xffffffff)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_7: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_8: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_9: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    roll_speed: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    phazon_weak_point_health: float = dataclasses.field(default=0.0)
    rock_weak_point_health: float = dataclasses.field(default=0.0)
    ice_spikes_speed: float = dataclasses.field(default=0.0)
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=0xffffffff)
    unknown_9: AssetId = dataclasses.field(default=0x0)
    particle_10: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    unknown_10: AssetId = dataclasses.field(default=0x0)
    unknown_11: AssetId = dataclasses.field(default=0x0)
    unknown_12: AssetId = dataclasses.field(default=0x0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x58

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
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>?', data.read(1))[0]
        rock_weak_point_1_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_2_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_3_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_4_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_5_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_6_model = struct.unpack(">L", data.read(4))[0]
        rock_weak_point_7_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_1_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_2_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_3_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_4_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_5_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_6_model = struct.unpack(">L", data.read(4))[0]
        phazon_weak_point_7_model = struct.unpack(">L", data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        state_machine = struct.unpack(">L", data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        particle_5 = struct.unpack(">L", data.read(4))[0]
        particle_6 = struct.unpack(">L", data.read(4))[0]
        particle_7 = struct.unpack(">L", data.read(4))[0]
        particle_8 = struct.unpack(">L", data.read(4))[0]
        particle_9 = struct.unpack(">L", data.read(4))[0]
        roll_speed = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        phazon_weak_point_health = struct.unpack('>f', data.read(4))[0]
        rock_weak_point_health = struct.unpack('>f', data.read(4))[0]
        ice_spikes_speed = struct.unpack('>f', data.read(4))[0]
        texture = struct.unpack(">L", data.read(4))[0]
        unknown_9 = struct.unpack(">L", data.read(4))[0]
        particle_10 = struct.unpack(">L", data.read(4))[0]
        unknown_10 = struct.unpack(">L", data.read(4))[0]
        unknown_11 = struct.unpack(">L", data.read(4))[0]
        unknown_12 = struct.unpack(">L", data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, unknown_1, unknown_2, rock_weak_point_1_model, rock_weak_point_2_model, rock_weak_point_3_model, rock_weak_point_4_model, rock_weak_point_5_model, rock_weak_point_6_model, rock_weak_point_7_model, phazon_weak_point_1_model, phazon_weak_point_2_model, phazon_weak_point_3_model, phazon_weak_point_4_model, phazon_weak_point_5_model, phazon_weak_point_6_model, phazon_weak_point_7_model, particle_1, particle_2, particle_3, state_machine, particle_4, particle_5, particle_6, particle_7, particle_8, particle_9, roll_speed, unknown_4, unknown_5, phazon_weak_point_health, rock_weak_point_health, ice_spikes_speed, texture, unknown_9, particle_10, unknown_10, unknown_11, unknown_12)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00,')  # 44 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack(">L", self.rock_weak_point_1_model))
        data.write(struct.pack(">L", self.rock_weak_point_2_model))
        data.write(struct.pack(">L", self.rock_weak_point_3_model))
        data.write(struct.pack(">L", self.rock_weak_point_4_model))
        data.write(struct.pack(">L", self.rock_weak_point_5_model))
        data.write(struct.pack(">L", self.rock_weak_point_6_model))
        data.write(struct.pack(">L", self.rock_weak_point_7_model))
        data.write(struct.pack(">L", self.phazon_weak_point_1_model))
        data.write(struct.pack(">L", self.phazon_weak_point_2_model))
        data.write(struct.pack(">L", self.phazon_weak_point_3_model))
        data.write(struct.pack(">L", self.phazon_weak_point_4_model))
        data.write(struct.pack(">L", self.phazon_weak_point_5_model))
        data.write(struct.pack(">L", self.phazon_weak_point_6_model))
        data.write(struct.pack(">L", self.phazon_weak_point_7_model))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.particle_3))
        data.write(struct.pack(">L", self.state_machine))
        data.write(struct.pack(">L", self.particle_4))
        data.write(struct.pack(">L", self.particle_5))
        data.write(struct.pack(">L", self.particle_6))
        data.write(struct.pack(">L", self.particle_7))
        data.write(struct.pack(">L", self.particle_8))
        data.write(struct.pack(">L", self.particle_9))
        data.write(struct.pack('>f', self.roll_speed))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.phazon_weak_point_health))
        data.write(struct.pack('>f', self.rock_weak_point_health))
        data.write(struct.pack('>f', self.ice_spikes_speed))
        data.write(struct.pack(">L", self.texture))
        data.write(struct.pack(">L", self.unknown_9))
        data.write(struct.pack(">L", self.particle_10))
        data.write(struct.pack(">L", self.unknown_10))
        data.write(struct.pack(">L", self.unknown_11))
        data.write(struct.pack(">L", self.unknown_12))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            rock_weak_point_1_model=data['rock_weak_point_1_model'],
            rock_weak_point_2_model=data['rock_weak_point_2_model'],
            rock_weak_point_3_model=data['rock_weak_point_3_model'],
            rock_weak_point_4_model=data['rock_weak_point_4_model'],
            rock_weak_point_5_model=data['rock_weak_point_5_model'],
            rock_weak_point_6_model=data['rock_weak_point_6_model'],
            rock_weak_point_7_model=data['rock_weak_point_7_model'],
            phazon_weak_point_1_model=data['phazon_weak_point_1_model'],
            phazon_weak_point_2_model=data['phazon_weak_point_2_model'],
            phazon_weak_point_3_model=data['phazon_weak_point_3_model'],
            phazon_weak_point_4_model=data['phazon_weak_point_4_model'],
            phazon_weak_point_5_model=data['phazon_weak_point_5_model'],
            phazon_weak_point_6_model=data['phazon_weak_point_6_model'],
            phazon_weak_point_7_model=data['phazon_weak_point_7_model'],
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            particle_3=data['particle_3'],
            state_machine=data['state_machine'],
            particle_4=data['particle_4'],
            particle_5=data['particle_5'],
            particle_6=data['particle_6'],
            particle_7=data['particle_7'],
            particle_8=data['particle_8'],
            particle_9=data['particle_9'],
            roll_speed=data['roll_speed'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            phazon_weak_point_health=data['phazon_weak_point_health'],
            rock_weak_point_health=data['rock_weak_point_health'],
            ice_spikes_speed=data['ice_spikes_speed'],
            texture=data['texture'],
            unknown_9=data['unknown_9'],
            particle_10=data['particle_10'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'rock_weak_point_1_model': self.rock_weak_point_1_model,
            'rock_weak_point_2_model': self.rock_weak_point_2_model,
            'rock_weak_point_3_model': self.rock_weak_point_3_model,
            'rock_weak_point_4_model': self.rock_weak_point_4_model,
            'rock_weak_point_5_model': self.rock_weak_point_5_model,
            'rock_weak_point_6_model': self.rock_weak_point_6_model,
            'rock_weak_point_7_model': self.rock_weak_point_7_model,
            'phazon_weak_point_1_model': self.phazon_weak_point_1_model,
            'phazon_weak_point_2_model': self.phazon_weak_point_2_model,
            'phazon_weak_point_3_model': self.phazon_weak_point_3_model,
            'phazon_weak_point_4_model': self.phazon_weak_point_4_model,
            'phazon_weak_point_5_model': self.phazon_weak_point_5_model,
            'phazon_weak_point_6_model': self.phazon_weak_point_6_model,
            'phazon_weak_point_7_model': self.phazon_weak_point_7_model,
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'particle_3': self.particle_3,
            'state_machine': self.state_machine,
            'particle_4': self.particle_4,
            'particle_5': self.particle_5,
            'particle_6': self.particle_6,
            'particle_7': self.particle_7,
            'particle_8': self.particle_8,
            'particle_9': self.particle_9,
            'roll_speed': self.roll_speed,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'phazon_weak_point_health': self.phazon_weak_point_health,
            'rock_weak_point_health': self.rock_weak_point_health,
            'ice_spikes_speed': self.ice_spikes_speed,
            'texture': self.texture,
            'unknown_9': self.unknown_9,
            'particle_10': self.particle_10,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
        }
