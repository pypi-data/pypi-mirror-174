# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.FargullHatcherSwarmData import FargullHatcherSwarmData
from retro_data_structures.properties.corruption.archetypes.FlyerSwarmData import FlyerSwarmData
from retro_data_structures.properties.corruption.archetypes.SwarmBasicsData import SwarmBasicsData
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class FargullHatcherSwarm(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    active: bool = dataclasses.field(default=True)
    swarm_basics_data: SwarmBasicsData = dataclasses.field(default_factory=SwarmBasicsData)
    flyer_swarm_data: FlyerSwarmData = dataclasses.field(default_factory=FlyerSwarmData)
    fargull_hatcher_swarm_data: FargullHatcherSwarmData = dataclasses.field(default_factory=FargullHatcherSwarmData)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def object_type(cls) -> str:
        return 'FGHS'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_FargullHatcherSwarm.rso']

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

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbb/E')  # 0xc6bb2f45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.active))

        data.write(b'L\xfcF\xfe')  # 0x4cfc46fe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.swarm_basics_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x99\xc1\x87\x02')  # 0x99c18702
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_swarm_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x14ou\xd9')  # 0x146f75d9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fargull_hatcher_swarm_data.to_stream(data)
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
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            active=data['active'],
            swarm_basics_data=SwarmBasicsData.from_json(data['swarm_basics_data']),
            flyer_swarm_data=FlyerSwarmData.from_json(data['flyer_swarm_data']),
            fargull_hatcher_swarm_data=FargullHatcherSwarmData.from_json(data['fargull_hatcher_swarm_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'character_animation_information': self.character_animation_information.to_json(),
            'active': self.active,
            'swarm_basics_data': self.swarm_basics_data.to_json(),
            'flyer_swarm_data': self.flyer_swarm_data.to_json(),
            'fargull_hatcher_swarm_data': self.fargull_hatcher_swarm_data.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_swarm_basics_data(data: typing.BinaryIO, property_size: int):
    return SwarmBasicsData.from_stream(data, property_size)


def _decode_flyer_swarm_data(data: typing.BinaryIO, property_size: int):
    return FlyerSwarmData.from_stream(data, property_size)


def _decode_fargull_hatcher_swarm_data(data: typing.BinaryIO, property_size: int):
    return FargullHatcherSwarmData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xc6bb2f45: ('active', _decode_active),
    0x4cfc46fe: ('swarm_basics_data', _decode_swarm_basics_data),
    0x99c18702: ('flyer_swarm_data', _decode_flyer_swarm_data),
    0x146f75d9: ('fargull_hatcher_swarm_data', _decode_fargull_hatcher_swarm_data),
}
