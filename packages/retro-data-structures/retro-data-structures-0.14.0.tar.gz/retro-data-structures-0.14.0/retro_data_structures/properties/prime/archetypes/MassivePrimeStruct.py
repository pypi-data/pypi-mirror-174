# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.archetypes.PrimeStruct2 import PrimeStruct2
from retro_data_structures.properties.prime.archetypes.PrimeStruct4 import PrimeStruct4
from retro_data_structures.properties.prime.archetypes.PrimeStruct6 import PrimeStruct6
from retro_data_structures.properties.prime.core.AssetId import AssetId


@dataclasses.dataclass()
class MassivePrimeStruct(BaseProperty):
    unknown_1: int = dataclasses.field(default=0)
    unnamed_0x00000001: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000002: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_2: int = dataclasses.field(default=0)
    prime_struct2_1: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    prime_struct2_2: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    prime_struct2_3: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    unknown_3: int = dataclasses.field(default=0)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    damage_info_1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    texture_1: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=0xffffffff)
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: AssetId = dataclasses.field(default=0x0)
    particle_4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    prime_struct4_1: PrimeStruct4 = dataclasses.field(default_factory=PrimeStruct4)
    prime_struct4_2: PrimeStruct4 = dataclasses.field(default_factory=PrimeStruct4)
    prime_struct4_3: PrimeStruct4 = dataclasses.field(default_factory=PrimeStruct4)
    prime_struct4_4: PrimeStruct4 = dataclasses.field(default_factory=PrimeStruct4)
    wpsc_1: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    damage_info_2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    prime_struct2_4: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    wpsc_2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    damage_info_3: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    prime_struct2_5: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    unknown_8: int = dataclasses.field(default=0)
    particle_5: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    damage_info_4: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: float = dataclasses.field(default=0.0)
    texture_2: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=0xffffffff)
    unknown_12: bool = dataclasses.field(default=False)
    unknown_13: bool = dataclasses.field(default=False)
    unknown_14: bool = dataclasses.field(default=False)
    unknown_15: bool = dataclasses.field(default=False)
    damage_info_5: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    prime_struct2_6: PrimeStruct2 = dataclasses.field(default_factory=PrimeStruct2)
    particle_6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    swhc: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=0xffffffff)
    particle_7: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_8: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    prime_struct6_1: PrimeStruct6 = dataclasses.field(default_factory=PrimeStruct6)
    prime_struct6_2: PrimeStruct6 = dataclasses.field(default_factory=PrimeStruct6)
    prime_struct6_3: PrimeStruct6 = dataclasses.field(default_factory=PrimeStruct6)
    prime_struct6_4: PrimeStruct6 = dataclasses.field(default_factory=PrimeStruct6)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        unnamed_0x00000001 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000002 = ActorParameters.from_stream(data, property_size)
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        prime_struct2_1 = PrimeStruct2.from_stream(data, property_size)
        prime_struct2_2 = PrimeStruct2.from_stream(data, property_size)
        prime_struct2_3 = PrimeStruct2.from_stream(data, property_size)
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        damage_info_1 = DamageInfo.from_stream(data, property_size)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        texture_1 = struct.unpack(">L", data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack(">L", data.read(4))[0]
        particle_4 = struct.unpack(">L", data.read(4))[0]
        prime_struct4_1 = PrimeStruct4.from_stream(data, property_size)
        prime_struct4_2 = PrimeStruct4.from_stream(data, property_size)
        prime_struct4_3 = PrimeStruct4.from_stream(data, property_size)
        prime_struct4_4 = PrimeStruct4.from_stream(data, property_size)
        wpsc_1 = struct.unpack(">L", data.read(4))[0]
        damage_info_2 = DamageInfo.from_stream(data, property_size)
        prime_struct2_4 = PrimeStruct2.from_stream(data, property_size)
        wpsc_2 = struct.unpack(">L", data.read(4))[0]
        damage_info_3 = DamageInfo.from_stream(data, property_size)
        prime_struct2_5 = PrimeStruct2.from_stream(data, property_size)
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        particle_5 = struct.unpack(">L", data.read(4))[0]
        damage_info_4 = DamageInfo.from_stream(data, property_size)
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>f', data.read(4))[0]
        texture_2 = struct.unpack(">L", data.read(4))[0]
        unknown_12 = struct.unpack('>?', data.read(1))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        unknown_14 = struct.unpack('>?', data.read(1))[0]
        unknown_15 = struct.unpack('>?', data.read(1))[0]
        damage_info_5 = DamageInfo.from_stream(data, property_size)
        prime_struct2_6 = PrimeStruct2.from_stream(data, property_size)
        particle_6 = struct.unpack(">L", data.read(4))[0]
        swhc = struct.unpack(">L", data.read(4))[0]
        particle_7 = struct.unpack(">L", data.read(4))[0]
        particle_8 = struct.unpack(">L", data.read(4))[0]
        prime_struct6_1 = PrimeStruct6.from_stream(data, property_size)
        prime_struct6_2 = PrimeStruct6.from_stream(data, property_size)
        prime_struct6_3 = PrimeStruct6.from_stream(data, property_size)
        prime_struct6_4 = PrimeStruct6.from_stream(data, property_size)
        return cls(unknown_1, unnamed_0x00000001, unnamed_0x00000002, unknown_2, prime_struct2_1, prime_struct2_2, prime_struct2_3, unknown_3, particle_1, particle_2, particle_3, damage_info_1, unknown_4, unknown_5, texture_1, unknown_6, unknown_7, particle_4, prime_struct4_1, prime_struct4_2, prime_struct4_3, prime_struct4_4, wpsc_1, damage_info_2, prime_struct2_4, wpsc_2, damage_info_3, prime_struct2_5, unknown_8, particle_5, damage_info_4, unknown_9, unknown_10, unknown_11, texture_2, unknown_12, unknown_13, unknown_14, unknown_15, damage_info_5, prime_struct2_6, particle_6, swhc, particle_7, particle_8, prime_struct6_1, prime_struct6_2, prime_struct6_3, prime_struct6_4)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>l', self.unknown_1))
        self.unnamed_0x00000001.to_stream(data)
        self.unnamed_0x00000002.to_stream(data)
        data.write(struct.pack('>l', self.unknown_2))
        self.prime_struct2_1.to_stream(data)
        self.prime_struct2_2.to_stream(data)
        self.prime_struct2_3.to_stream(data)
        data.write(struct.pack('>l', self.unknown_3))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack(">L", self.particle_3))
        self.damage_info_1.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack(">L", self.texture_1))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack(">L", self.unknown_7))
        data.write(struct.pack(">L", self.particle_4))
        self.prime_struct4_1.to_stream(data)
        self.prime_struct4_2.to_stream(data)
        self.prime_struct4_3.to_stream(data)
        self.prime_struct4_4.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_1))
        self.damage_info_2.to_stream(data)
        self.prime_struct2_4.to_stream(data)
        data.write(struct.pack(">L", self.wpsc_2))
        self.damage_info_3.to_stream(data)
        self.prime_struct2_5.to_stream(data)
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack(">L", self.particle_5))
        self.damage_info_4.to_stream(data)
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>f', self.unknown_11))
        data.write(struct.pack(">L", self.texture_2))
        data.write(struct.pack('>?', self.unknown_12))
        data.write(struct.pack('>?', self.unknown_13))
        data.write(struct.pack('>?', self.unknown_14))
        data.write(struct.pack('>?', self.unknown_15))
        self.damage_info_5.to_stream(data)
        self.prime_struct2_6.to_stream(data)
        data.write(struct.pack(">L", self.particle_6))
        data.write(struct.pack(">L", self.swhc))
        data.write(struct.pack(">L", self.particle_7))
        data.write(struct.pack(">L", self.particle_8))
        self.prime_struct6_1.to_stream(data)
        self.prime_struct6_2.to_stream(data)
        self.prime_struct6_3.to_stream(data)
        self.prime_struct6_4.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unnamed_0x00000001=PatternedAITypedef.from_json(data['unnamed_0x00000001']),
            unnamed_0x00000002=ActorParameters.from_json(data['unnamed_0x00000002']),
            unknown_2=data['unknown_2'],
            prime_struct2_1=PrimeStruct2.from_json(data['prime_struct2_1']),
            prime_struct2_2=PrimeStruct2.from_json(data['prime_struct2_2']),
            prime_struct2_3=PrimeStruct2.from_json(data['prime_struct2_3']),
            unknown_3=data['unknown_3'],
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            particle_3=data['particle_3'],
            damage_info_1=DamageInfo.from_json(data['damage_info_1']),
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            texture_1=data['texture_1'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            particle_4=data['particle_4'],
            prime_struct4_1=PrimeStruct4.from_json(data['prime_struct4_1']),
            prime_struct4_2=PrimeStruct4.from_json(data['prime_struct4_2']),
            prime_struct4_3=PrimeStruct4.from_json(data['prime_struct4_3']),
            prime_struct4_4=PrimeStruct4.from_json(data['prime_struct4_4']),
            wpsc_1=data['wpsc_1'],
            damage_info_2=DamageInfo.from_json(data['damage_info_2']),
            prime_struct2_4=PrimeStruct2.from_json(data['prime_struct2_4']),
            wpsc_2=data['wpsc_2'],
            damage_info_3=DamageInfo.from_json(data['damage_info_3']),
            prime_struct2_5=PrimeStruct2.from_json(data['prime_struct2_5']),
            unknown_8=data['unknown_8'],
            particle_5=data['particle_5'],
            damage_info_4=DamageInfo.from_json(data['damage_info_4']),
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            texture_2=data['texture_2'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            damage_info_5=DamageInfo.from_json(data['damage_info_5']),
            prime_struct2_6=PrimeStruct2.from_json(data['prime_struct2_6']),
            particle_6=data['particle_6'],
            swhc=data['swhc'],
            particle_7=data['particle_7'],
            particle_8=data['particle_8'],
            prime_struct6_1=PrimeStruct6.from_json(data['prime_struct6_1']),
            prime_struct6_2=PrimeStruct6.from_json(data['prime_struct6_2']),
            prime_struct6_3=PrimeStruct6.from_json(data['prime_struct6_3']),
            prime_struct6_4=PrimeStruct6.from_json(data['prime_struct6_4']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unnamed_0x00000001': self.unnamed_0x00000001.to_json(),
            'unnamed_0x00000002': self.unnamed_0x00000002.to_json(),
            'unknown_2': self.unknown_2,
            'prime_struct2_1': self.prime_struct2_1.to_json(),
            'prime_struct2_2': self.prime_struct2_2.to_json(),
            'prime_struct2_3': self.prime_struct2_3.to_json(),
            'unknown_3': self.unknown_3,
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'particle_3': self.particle_3,
            'damage_info_1': self.damage_info_1.to_json(),
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'texture_1': self.texture_1,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'particle_4': self.particle_4,
            'prime_struct4_1': self.prime_struct4_1.to_json(),
            'prime_struct4_2': self.prime_struct4_2.to_json(),
            'prime_struct4_3': self.prime_struct4_3.to_json(),
            'prime_struct4_4': self.prime_struct4_4.to_json(),
            'wpsc_1': self.wpsc_1,
            'damage_info_2': self.damage_info_2.to_json(),
            'prime_struct2_4': self.prime_struct2_4.to_json(),
            'wpsc_2': self.wpsc_2,
            'damage_info_3': self.damage_info_3.to_json(),
            'prime_struct2_5': self.prime_struct2_5.to_json(),
            'unknown_8': self.unknown_8,
            'particle_5': self.particle_5,
            'damage_info_4': self.damage_info_4.to_json(),
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'texture_2': self.texture_2,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'damage_info_5': self.damage_info_5.to_json(),
            'prime_struct2_6': self.prime_struct2_6.to_json(),
            'particle_6': self.particle_6,
            'swhc': self.swhc,
            'particle_7': self.particle_7,
            'particle_8': self.particle_8,
            'prime_struct6_1': self.prime_struct6_1.to_json(),
            'prime_struct6_2': self.prime_struct6_2.to_json(),
            'prime_struct6_3': self.prime_struct6_3.to_json(),
            'prime_struct6_4': self.prime_struct6_4.to_json(),
        }
