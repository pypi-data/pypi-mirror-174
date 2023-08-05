# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SurroundPan import SurroundPan
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class Sound(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    sound: AssetId = dataclasses.field(default=0x0)
    max_audible_distance: float = dataclasses.field(default=50.0)
    drop_off: float = dataclasses.field(default=0.20000000298023224)
    delay_time: float = dataclasses.field(default=0.0)
    min_volume: int = dataclasses.field(default=20)
    max_volume: int = dataclasses.field(default=127)
    priority: int = dataclasses.field(default=127)
    surround_pan: SurroundPan = dataclasses.field(default_factory=SurroundPan)
    loop: bool = dataclasses.field(default=False)
    ambient: bool = dataclasses.field(default=False)
    unknown: bool = dataclasses.field(default=False)
    auto_start: bool = dataclasses.field(default=False)
    can_occlude: bool = dataclasses.field(default=False)
    use_room_acoustics: bool = dataclasses.field(default=True)
    persistent: bool = dataclasses.field(default=False)
    play_always: bool = dataclasses.field(default=False)
    all_area: bool = dataclasses.field(default=False)
    sound_is_music: bool = dataclasses.field(default=False)
    pitch: int = dataclasses.field(default=0)
    echo_visor_max_volume: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'SOND'

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_|5.')  # 0x5f7c352e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'\x08\xbf.T')  # 0x8bf2e54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_off))

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'Wa\x94\x96')  # 0x57619496
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_volume))

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\x0b\xb6&9')  # 0xbb62639
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surround_pan.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'\x89q\xb7\xa7')  # 0x8971b7a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ambient))

        data.write(b'\x84\xf3\xac=')  # 0x84f3ac3d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'\x94r\x11c')  # 0x94721163
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_occlude))

        data.write(b'\x85psT')  # 0x85707354
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_room_acoustics))

        data.write(b'\xea\x03\xe2X')  # 0xea03e258
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.persistent))

        data.write(b'\r\x7f\x8c\x7f')  # 0xd7f8c7f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_always))

        data.write(b'\xe4\\4\x99')  # 0xe45c3499
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.all_area))

        data.write(b'v\xd4\x00\x91')  # 0x76d40091
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sound_is_music))

        data.write(b'\x8avDc')  # 0x8a764463
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.pitch))

        data.write(b'i\xec\x91\x07')  # 0x69ec9107
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.echo_visor_max_volume))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            sound=data['sound'],
            max_audible_distance=data['max_audible_distance'],
            drop_off=data['drop_off'],
            delay_time=data['delay_time'],
            min_volume=data['min_volume'],
            max_volume=data['max_volume'],
            priority=data['priority'],
            surround_pan=SurroundPan.from_json(data['surround_pan']),
            loop=data['loop'],
            ambient=data['ambient'],
            unknown=data['unknown'],
            auto_start=data['auto_start'],
            can_occlude=data['can_occlude'],
            use_room_acoustics=data['use_room_acoustics'],
            persistent=data['persistent'],
            play_always=data['play_always'],
            all_area=data['all_area'],
            sound_is_music=data['sound_is_music'],
            pitch=data['pitch'],
            echo_visor_max_volume=data['echo_visor_max_volume'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'sound': self.sound,
            'max_audible_distance': self.max_audible_distance,
            'drop_off': self.drop_off,
            'delay_time': self.delay_time,
            'min_volume': self.min_volume,
            'max_volume': self.max_volume,
            'priority': self.priority,
            'surround_pan': self.surround_pan.to_json(),
            'loop': self.loop,
            'ambient': self.ambient,
            'unknown': self.unknown,
            'auto_start': self.auto_start,
            'can_occlude': self.can_occlude,
            'use_room_acoustics': self.use_room_acoustics,
            'persistent': self.persistent,
            'play_always': self.play_always,
            'all_area': self.all_area,
            'sound_is_music': self.sound_is_music,
            'pitch': self.pitch,
            'echo_visor_max_volume': self.echo_visor_max_volume,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_off(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_surround_pan(data: typing.BinaryIO, property_size: int):
    return SurroundPan.from_stream(data, property_size)


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ambient(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_occlude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_room_acoustics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_persistent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_play_always(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_all_area(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_is_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_echo_visor_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x5f7c352e: ('sound', _decode_sound),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x8bf2e54: ('drop_off', _decode_drop_off),
    0x8e16e012: ('delay_time', _decode_delay_time),
    0x57619496: ('min_volume', _decode_min_volume),
    0xc712847c: ('max_volume', _decode_max_volume),
    0x42087650: ('priority', _decode_priority),
    0xbb62639: ('surround_pan', _decode_surround_pan),
    0xeda47ff6: ('loop', _decode_loop),
    0x8971b7a7: ('ambient', _decode_ambient),
    0x84f3ac3d: ('unknown', _decode_unknown),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x94721163: ('can_occlude', _decode_can_occlude),
    0x85707354: ('use_room_acoustics', _decode_use_room_acoustics),
    0xea03e258: ('persistent', _decode_persistent),
    0xd7f8c7f: ('play_always', _decode_play_always),
    0xe45c3499: ('all_area', _decode_all_area),
    0x76d40091: ('sound_is_music', _decode_sound_is_music),
    0x8a764463: ('pitch', _decode_pitch),
    0x69ec9107: ('echo_visor_max_volume', _decode_echo_visor_max_volume),
}
