# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Glowbug(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    death_flash_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    attack_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC']}, default=0xffffffff)
    attack_telegraph_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    attack_echo_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    attack_duration: float = dataclasses.field(default=1.0)
    attack_telegraph_duration: float = dataclasses.field(default=1.0)
    attack_aim_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    attack_telegraph_sound: AssetId = dataclasses.field(default=0x0)
    attack_sound: AssetId = dataclasses.field(default=0x0)
    scan_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    is_in_light_world: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'GBUG'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Glowbug.rel']

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
        data.write(b'\x00\x0f')  # 15 properties

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
        self.patterned.to_stream(data)
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

        data.write(b'\xd7T&\xf9')  # 0xd75426f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_flash_effect))

        data.write(b'\x89\x85\xb39')  # 0x8985b339
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'\xb2X\xd3\xe8')  # 0xb258d3e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.attack_effect))

        data.write(b'\xb0h\x15\xb3')  # 0xb06815b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.attack_telegraph_effect))

        data.write(b'\xab7\x8ad')  # 0xab378a64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.attack_echo_effect))

        data.write(b'\x164,\x18')  # 0x16342c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_duration))

        data.write(b'=|\xcd2')  # 0x3d7ccd32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_telegraph_duration))

        data.write(b'T\x0c\x1f\x87')  # 0x540c1f87
        data.write(b'\x00\x0c')  # size
        self.attack_aim_offset.to_stream(data)

        data.write(b'\r\xb1\x0fk')  # 0xdb10f6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.attack_telegraph_sound))

        data.write(b'P\xe4^\xa8')  # 0x50e45ea8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.attack_sound))

        data.write(b'\xa9H.\xb1')  # 0xa9482eb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scan_model))

        data.write(b'\x19\x17\xa1\x80')  # 0x1917a180
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_in_light_world))

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
            death_flash_effect=data['death_flash_effect'],
            part=data['part'],
            attack_effect=data['attack_effect'],
            attack_telegraph_effect=data['attack_telegraph_effect'],
            attack_echo_effect=data['attack_echo_effect'],
            attack_duration=data['attack_duration'],
            attack_telegraph_duration=data['attack_telegraph_duration'],
            attack_aim_offset=Vector.from_json(data['attack_aim_offset']),
            attack_telegraph_sound=data['attack_telegraph_sound'],
            attack_sound=data['attack_sound'],
            scan_model=data['scan_model'],
            is_in_light_world=data['is_in_light_world'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'death_flash_effect': self.death_flash_effect,
            'part': self.part,
            'attack_effect': self.attack_effect,
            'attack_telegraph_effect': self.attack_telegraph_effect,
            'attack_echo_effect': self.attack_echo_effect,
            'attack_duration': self.attack_duration,
            'attack_telegraph_duration': self.attack_telegraph_duration,
            'attack_aim_offset': self.attack_aim_offset.to_json(),
            'attack_telegraph_sound': self.attack_telegraph_sound,
            'attack_sound': self.attack_sound,
            'scan_model': self.scan_model,
            'is_in_light_world': self.is_in_light_world,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_death_flash_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_telegraph_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_echo_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_telegraph_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_aim_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_attack_telegraph_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scan_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_is_in_light_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xd75426f9: ('death_flash_effect', _decode_death_flash_effect),
    0x8985b339: ('part', _decode_part),
    0xb258d3e8: ('attack_effect', _decode_attack_effect),
    0xb06815b3: ('attack_telegraph_effect', _decode_attack_telegraph_effect),
    0xab378a64: ('attack_echo_effect', _decode_attack_echo_effect),
    0x16342c18: ('attack_duration', _decode_attack_duration),
    0x3d7ccd32: ('attack_telegraph_duration', _decode_attack_telegraph_duration),
    0x540c1f87: ('attack_aim_offset', _decode_attack_aim_offset),
    0xdb10f6b: ('attack_telegraph_sound', _decode_attack_telegraph_sound),
    0x50e45ea8: ('attack_sound', _decode_attack_sound),
    0xa9482eb1: ('scan_model', _decode_scan_model),
    0x1917a180: ('is_in_light_world', _decode_is_in_light_world),
}
