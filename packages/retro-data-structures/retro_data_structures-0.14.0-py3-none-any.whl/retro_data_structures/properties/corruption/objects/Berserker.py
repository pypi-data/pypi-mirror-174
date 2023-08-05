# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.BerserkerData import BerserkerData
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.UnknownStruct21 import UnknownStruct21


@dataclasses.dataclass()
class Berserker(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    patterned_info: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    berserker_info: BerserkerData = dataclasses.field(default_factory=BerserkerData)
    berserker_info_hard: BerserkerData = dataclasses.field(default_factory=BerserkerData)
    berserker_info_elite: BerserkerData = dataclasses.field(default_factory=BerserkerData)
    unknown_struct21: UnknownStruct21 = dataclasses.field(default_factory=UnknownStruct21)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def object_type(cls) -> str:
        return 'BSKR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_Berserker.rso']

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'C\xbb\xb1\xdd')  # 0x43bbb1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_info.to_stream(data, default_override={'damage_wait_time': 3.0, 'step_up_height': 1.0, 'creature_size': 2, 'turn_speed': 180.0, 'detection_range': 50.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\xf9\xff\xa5')  # 0x54f9ffa5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.berserker_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\x8d\xc0\xaf')  # 0x2d8dc0af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.berserker_info_hard.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x0c\xe8(')  # 0xe10ce828
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.berserker_info_elite.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{\x8cH\xc7')  # 0x7b8c48c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct21.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            patterned_info=PatternedAITypedef.from_json(data['patterned_info']),
            berserker_info=BerserkerData.from_json(data['berserker_info']),
            berserker_info_hard=BerserkerData.from_json(data['berserker_info_hard']),
            berserker_info_elite=BerserkerData.from_json(data['berserker_info_elite']),
            unknown_struct21=UnknownStruct21.from_json(data['unknown_struct21']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'patterned_info': self.patterned_info.to_json(),
            'berserker_info': self.berserker_info.to_json(),
            'berserker_info_hard': self.berserker_info_hard.to_json(),
            'berserker_info_elite': self.berserker_info_elite.to_json(),
            'unknown_struct21': self.unknown_struct21.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_patterned_info(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'damage_wait_time': 3.0, 'step_up_height': 1.0, 'creature_size': 2, 'turn_speed': 180.0, 'detection_range': 50.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5})


def _decode_berserker_info(data: typing.BinaryIO, property_size: int):
    return BerserkerData.from_stream(data, property_size)


def _decode_berserker_info_hard(data: typing.BinaryIO, property_size: int):
    return BerserkerData.from_stream(data, property_size)


def _decode_berserker_info_elite(data: typing.BinaryIO, property_size: int):
    return BerserkerData.from_stream(data, property_size)


def _decode_unknown_struct21(data: typing.BinaryIO, property_size: int):
    return UnknownStruct21.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x43bbb1dd: ('patterned_info', _decode_patterned_info),
    0x54f9ffa5: ('berserker_info', _decode_berserker_info),
    0x2d8dc0af: ('berserker_info_hard', _decode_berserker_info_hard),
    0xe10ce828: ('berserker_info_elite', _decode_berserker_info_elite),
    0x7b8c48c7: ('unknown_struct21', _decode_unknown_struct21),
}
