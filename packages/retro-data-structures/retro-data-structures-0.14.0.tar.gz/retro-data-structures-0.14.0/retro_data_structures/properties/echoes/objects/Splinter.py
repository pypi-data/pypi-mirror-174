# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class Splinter(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x72edeb7d: float = dataclasses.field(default=0.0)
    unknown_0xb8ed9ffa: float = dataclasses.field(default=5.0)
    unknown_0x5e8d301b: float = dataclasses.field(default=18.0)
    unknown_0xb98bb88f: float = dataclasses.field(default=1.0)
    unknown_0x5feb176e: float = dataclasses.field(default=3.0)
    unknown_0x726cd31d: int = dataclasses.field(default=1)
    unknown_0x376e909f: int = dataclasses.field(default=2)
    attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xb63b810c: int = dataclasses.field(default=0)
    unknown_0x6d752efc: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x0d6ab7b5: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    part_0x630d93a1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    damage_info_0x4436a388: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    is_mega_splinter: bool = dataclasses.field(default=False)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    damage_info_0x02fd0913: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0x496f191b: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    unknown_0x51be00d3: float = dataclasses.field(default=2.5)
    unknown_0xb7deaf32: float = dataclasses.field(default=5.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'SPTR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Splinter.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                data.read(property_size)  # skip unknown property
            assert data.tell() - start == property_size

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'detection_range': 32.0, 'min_attack_range': 7.0, 'max_attack_range': 17.0, 'collision_radius': 0.5, 'collision_height': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r\xed\xeb}')  # 0x72edeb7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72edeb7d))

        data.write(b'\xb8\xed\x9f\xfa')  # 0xb8ed9ffa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb8ed9ffa))

        data.write(b'^\x8d0\x1b')  # 0x5e8d301b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5e8d301b))

        data.write(b'\xb9\x8b\xb8\x8f')  # 0xb98bb88f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb98bb88f))

        data.write(b'_\xeb\x17n')  # 0x5feb176e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5feb176e))

        data.write(b'rl\xd3\x1d')  # 0x726cd31d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x726cd31d))

        data.write(b'7n\x90\x9f')  # 0x376e909f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x376e909f))

        data.write(b'f\xdc\xaa\xcb')  # 0x66dcaacb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6;\x81\x0c')  # 0xb63b810c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb63b810c))

        data.write(b'mu.\xfc')  # 0x6d752efc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x6d752efc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\rj\xb7\xb5')  # 0xd6ab7b5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x0d6ab7b5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\r\x93\xa1')  # 0x630d93a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x630d93a1))

        data.write(b'D6\xa3\x88')  # 0x4436a388
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x4436a388.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\xc8/F')  # 0x7dc82f46
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_mega_splinter))

        data.write(b'BQ\x83Y')  # 0x42518359
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.wpsc))

        data.write(b'\x02\xfd\t\x13')  # 0x2fd0913
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x02fd0913.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Io\x19\x1b')  # 0x496f191b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x496f191b))

        data.write(b'Q\xbe\x00\xd3')  # 0x51be00d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x51be00d3))

        data.write(b'\xb7\xde\xaf2')  # 0xb7deaf32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb7deaf32))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            unknown_0x72edeb7d=data['unknown_0x72edeb7d'],
            unknown_0xb8ed9ffa=data['unknown_0xb8ed9ffa'],
            unknown_0x5e8d301b=data['unknown_0x5e8d301b'],
            unknown_0xb98bb88f=data['unknown_0xb98bb88f'],
            unknown_0x5feb176e=data['unknown_0x5feb176e'],
            unknown_0x726cd31d=data['unknown_0x726cd31d'],
            unknown_0x376e909f=data['unknown_0x376e909f'],
            attack_damage=DamageInfo.from_json(data['attack_damage']),
            unknown_0xb63b810c=data['unknown_0xb63b810c'],
            unknown_0x6d752efc=AnimationParameters.from_json(data['unknown_0x6d752efc']),
            unknown_0x0d6ab7b5=AnimationParameters.from_json(data['unknown_0x0d6ab7b5']),
            part_0x630d93a1=data['part_0x630d93a1'],
            damage_info_0x4436a388=DamageInfo.from_json(data['damage_info_0x4436a388']),
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
            is_mega_splinter=data['is_mega_splinter'],
            wpsc=data['wpsc'],
            damage_info_0x02fd0913=DamageInfo.from_json(data['damage_info_0x02fd0913']),
            part_0x496f191b=data['part_0x496f191b'],
            unknown_0x51be00d3=data['unknown_0x51be00d3'],
            unknown_0xb7deaf32=data['unknown_0xb7deaf32'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x72edeb7d': self.unknown_0x72edeb7d,
            'unknown_0xb8ed9ffa': self.unknown_0xb8ed9ffa,
            'unknown_0x5e8d301b': self.unknown_0x5e8d301b,
            'unknown_0xb98bb88f': self.unknown_0xb98bb88f,
            'unknown_0x5feb176e': self.unknown_0x5feb176e,
            'unknown_0x726cd31d': self.unknown_0x726cd31d,
            'unknown_0x376e909f': self.unknown_0x376e909f,
            'attack_damage': self.attack_damage.to_json(),
            'unknown_0xb63b810c': self.unknown_0xb63b810c,
            'unknown_0x6d752efc': self.unknown_0x6d752efc.to_json(),
            'unknown_0x0d6ab7b5': self.unknown_0x0d6ab7b5.to_json(),
            'part_0x630d93a1': self.part_0x630d93a1,
            'damage_info_0x4436a388': self.damage_info_0x4436a388.to_json(),
            'ing_possession_data': self.ing_possession_data.to_json(),
            'is_mega_splinter': self.is_mega_splinter,
            'wpsc': self.wpsc,
            'damage_info_0x02fd0913': self.damage_info_0x02fd0913.to_json(),
            'part_0x496f191b': self.part_0x496f191b,
            'unknown_0x51be00d3': self.unknown_0x51be00d3,
            'unknown_0xb7deaf32': self.unknown_0xb7deaf32,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'detection_range': 32.0, 'min_attack_range': 7.0, 'max_attack_range': 17.0, 'collision_radius': 0.5, 'collision_height': 1.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x72edeb7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb8ed9ffa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5e8d301b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb98bb88f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5feb176e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x726cd31d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x376e909f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0xb63b810c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6d752efc(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x0d6ab7b5(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_part_0x630d93a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_info_0x4436a388(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_is_mega_splinter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_info_0x02fd0913(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_part_0x496f191b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x51be00d3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb7deaf32(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x72edeb7d: ('unknown_0x72edeb7d', _decode_unknown_0x72edeb7d),
    0xb8ed9ffa: ('unknown_0xb8ed9ffa', _decode_unknown_0xb8ed9ffa),
    0x5e8d301b: ('unknown_0x5e8d301b', _decode_unknown_0x5e8d301b),
    0xb98bb88f: ('unknown_0xb98bb88f', _decode_unknown_0xb98bb88f),
    0x5feb176e: ('unknown_0x5feb176e', _decode_unknown_0x5feb176e),
    0x726cd31d: ('unknown_0x726cd31d', _decode_unknown_0x726cd31d),
    0x376e909f: ('unknown_0x376e909f', _decode_unknown_0x376e909f),
    0x66dcaacb: ('attack_damage', _decode_attack_damage),
    0xb63b810c: ('unknown_0xb63b810c', _decode_unknown_0xb63b810c),
    0x6d752efc: ('unknown_0x6d752efc', _decode_unknown_0x6d752efc),
    0xd6ab7b5: ('unknown_0x0d6ab7b5', _decode_unknown_0x0d6ab7b5),
    0x630d93a1: ('part_0x630d93a1', _decode_part_0x630d93a1),
    0x4436a388: ('damage_info_0x4436a388', _decode_damage_info_0x4436a388),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x7dc82f46: ('is_mega_splinter', _decode_is_mega_splinter),
    0x42518359: ('wpsc', _decode_wpsc),
    0x2fd0913: ('damage_info_0x02fd0913', _decode_damage_info_0x02fd0913),
    0x496f191b: ('part_0x496f191b', _decode_part_0x496f191b),
    0x51be00d3: ('unknown_0x51be00d3', _decode_unknown_0x51be00d3),
    0xb7deaf32: ('unknown_0xb7deaf32', _decode_unknown_0xb7deaf32),
}
