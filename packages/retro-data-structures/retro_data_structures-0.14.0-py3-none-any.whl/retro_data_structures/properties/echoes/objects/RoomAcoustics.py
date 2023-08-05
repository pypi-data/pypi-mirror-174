# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class RoomAcoustics(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    room_volume: int = dataclasses.field(default=117)
    priority: int = dataclasses.field(default=1)  # Choice
    reverb_hi_enabled: bool = dataclasses.field(default=False)
    unknown_0x3263c26e: bool = dataclasses.field(default=False)
    reverb_hi_time: float = dataclasses.field(default=0.0)
    reverb_hi_pre_delay: float = dataclasses.field(default=0.0)
    reverb_hi_damping: float = dataclasses.field(default=0.0)
    reverb_hi_coloration: float = dataclasses.field(default=0.0)
    reverb_hi_cross_talk: float = dataclasses.field(default=0.0)
    reverb_hi_mix: float = dataclasses.field(default=0.0)
    chorus_enabled: bool = dataclasses.field(default=False)
    chorus_base_delay: float = dataclasses.field(default=0.0)
    chorus_variation: float = dataclasses.field(default=0.0)
    chorus_period: float = dataclasses.field(default=0.0)
    reverb_std_enabled: bool = dataclasses.field(default=False)
    unknown_0x4a5bbf90: bool = dataclasses.field(default=False)
    reverb_std_time: float = dataclasses.field(default=0.0)
    reverb_std_pre_delay: float = dataclasses.field(default=0.0)
    reverb_std_damping: float = dataclasses.field(default=0.0)
    reverb_std_coloration: float = dataclasses.field(default=0.0)
    reverb_std_mix: float = dataclasses.field(default=0.0)
    delay_enabled: bool = dataclasses.field(default=False)
    delay0: int = dataclasses.field(default=0)
    delay1: int = dataclasses.field(default=0)
    delay2: int = dataclasses.field(default=0)
    delay_feedback0: int = dataclasses.field(default=0)
    delay_feedback1: int = dataclasses.field(default=0)
    delay_feedback2: int = dataclasses.field(default=0)
    delay_output0: int = dataclasses.field(default=0)
    delay_output1: int = dataclasses.field(default=0)
    delay_output2: int = dataclasses.field(default=0)
    unknown_0xcf45711c: int = dataclasses.field(default=32000)
    unknown_0x626d1e9b: int = dataclasses.field(default=0)
    unknown_0x7d8ee273: bool = dataclasses.field(default=False)
    unknown_0x83378e6a: float = dataclasses.field(default=0.0)
    unknown_0xf549d269: float = dataclasses.field(default=0.0)
    unknown_0x11fdae16: float = dataclasses.field(default=0.0)
    unknown_0xa3c439c1: float = dataclasses.field(default=0.0)
    unknown_0x2dc70efe: float = dataclasses.field(default=0.0)
    unknown_0xe2bd3706: float = dataclasses.field(default=0.0)
    unknown_0x5e29cef8: float = dataclasses.field(default=0.0)
    unknown_0x35ae9f10: float = dataclasses.field(default=0.0)
    bitcrusher_enabled: bool = dataclasses.field(default=False)
    unknown_0xf51a1d6a: int = dataclasses.field(default=0)
    bitcrusher_gain: float = dataclasses.field(default=0.0)
    bitcrusher_bit_depth: int = dataclasses.field(default=0)
    unknown_0x58096e0b: float = dataclasses.field(default=1.0)
    phaser_enabled: bool = dataclasses.field(default=False)
    phaser_frequency: float = dataclasses.field(default=0.0)
    phaser_feedback: float = dataclasses.field(default=0.0)
    phaser_invert: float = dataclasses.field(default=0.0)
    phaser_mix: float = dataclasses.field(default=0.0)
    phaser_sweep: float = dataclasses.field(default=200.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'RMAC'

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
        data.write(b'\x006')  # 54 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\x9e\xa2f')  # 0xbd9ea266
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.room_volume))

        data.write(b'\x86\xcf#\xf4')  # 0x86cf23f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.priority))

        data.write(b'\xa0\x03`\xcc')  # 0xa00360cc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.reverb_hi_enabled))

        data.write(b'2c\xc2n')  # 0x3263c26e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x3263c26e))

        data.write(b'\xc5\x86\x80a')  # 0xc5868061
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_time))

        data.write(b'\xc6\xf5\x002')  # 0xc6f50032
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_pre_delay))

        data.write(b'\xcb\xa5U]')  # 0xcba5555d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_damping))

        data.write(b's\x19\xcfP')  # 0x7319cf50
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_coloration))

        data.write(b'=\xc3\xf1o')  # 0x3dc3f16f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_cross_talk))

        data.write(b'\xd5Q\x8bl')  # 0xd5518b6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_hi_mix))

        data.write(b'&\x99|\xcb')  # 0x26997ccb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.chorus_enabled))

        data.write(b'\x12\x1b\xdf\xad')  # 0x121bdfad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chorus_base_delay))

        data.write(b'\xe8yk\xce')  # 0xe8796bce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chorus_variation))

        data.write(b'$\xbb\xd5\xe4')  # 0x24bbd5e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chorus_period))

        data.write(b'\xff1c\x1b')  # 0xff31631b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.reverb_std_enabled))

        data.write(b'J[\xbf\x90')  # 0x4a5bbf90
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4a5bbf90))

        data.write(b'\x96bI\x8a')  # 0x9662498a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_std_time))

        data.write(b'\x91\x85]b')  # 0x91855d62
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_std_pre_delay))

        data.write(b'\xd3M )')  # 0xd34d2029
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_std_damping))

        data.write(b'\xdcx\xe8=')  # 0xdc78e83d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_std_coloration))

        data.write(b'\x82\x0bP\x9e')  # 0x820b509e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverb_std_mix))

        data.write(b'\xe9\xa3`1')  # 0xe9a36031
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.delay_enabled))

        data.write(b'b\xc4\x94W')  # 0x62c49457
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay0))

        data.write(b'\xdax\xf32')  # 0xda78f332
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay1))

        data.write(b'\xc8\xcd\\\xdc')  # 0xc8cd5cdc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay2))

        data.write(b'|\x14\xff\x17')  # 0x7c14ff17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_feedback0))

        data.write(b'\xc4\xa8\x98r')  # 0xc4a89872
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_feedback1))

        data.write(b'\xd6\x1d7\x9c')  # 0xd61d379c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_feedback2))

        data.write(b'\x9fu\x98\x7f')  # 0x9f75987f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_output0))

        data.write(b"'\xc9\xff\x1a")  # 0x27c9ff1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_output1))

        data.write(b'5|P\xf4')  # 0x357c50f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.delay_output2))

        data.write(b'\xcfEq\x1c')  # 0xcf45711c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xcf45711c))

        data.write(b'bm\x1e\x9b')  # 0x626d1e9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x626d1e9b))

        data.write(b'}\x8e\xe2s')  # 0x7d8ee273
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7d8ee273))

        data.write(b'\x837\x8ej')  # 0x83378e6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x83378e6a))

        data.write(b'\xf5I\xd2i')  # 0xf549d269
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf549d269))

        data.write(b'\x11\xfd\xae\x16')  # 0x11fdae16
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11fdae16))

        data.write(b'\xa3\xc49\xc1')  # 0xa3c439c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa3c439c1))

        data.write(b'-\xc7\x0e\xfe')  # 0x2dc70efe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2dc70efe))

        data.write(b'\xe2\xbd7\x06')  # 0xe2bd3706
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe2bd3706))

        data.write(b'^)\xce\xf8')  # 0x5e29cef8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5e29cef8))

        data.write(b'5\xae\x9f\x10')  # 0x35ae9f10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x35ae9f10))

        data.write(b'>\x8d\x86\x94')  # 0x3e8d8694
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.bitcrusher_enabled))

        data.write(b'\xf5\x1a\x1dj')  # 0xf51a1d6a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf51a1d6a))

        data.write(b'\xbb\x1a\x0f4')  # 0xbb1a0f34
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bitcrusher_gain))

        data.write(b'\xeb\x00\x909')  # 0xeb009039
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.bitcrusher_bit_depth))

        data.write(b'X\tn\x0b')  # 0x58096e0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x58096e0b))

        data.write(b'=\x8c\xad\x84')  # 0x3d8cad84
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.phaser_enabled))

        data.write(b'#\xc3@\xf6')  # 0x23c340f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phaser_frequency))

        data.write(b'\x1eZR\xb8')  # 0x1e5a52b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phaser_feedback))

        data.write(b'\x1di\xbe\xc4')  # 0x1d69bec4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phaser_invert))

        data.write(b'$S\x8cJ')  # 0x24538c4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phaser_mix))

        data.write(b'\xd58\x81\x16')  # 0xd5388116
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phaser_sweep))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            room_volume=data['room_volume'],
            priority=data['priority'],
            reverb_hi_enabled=data['reverb_hi_enabled'],
            unknown_0x3263c26e=data['unknown_0x3263c26e'],
            reverb_hi_time=data['reverb_hi_time'],
            reverb_hi_pre_delay=data['reverb_hi_pre_delay'],
            reverb_hi_damping=data['reverb_hi_damping'],
            reverb_hi_coloration=data['reverb_hi_coloration'],
            reverb_hi_cross_talk=data['reverb_hi_cross_talk'],
            reverb_hi_mix=data['reverb_hi_mix'],
            chorus_enabled=data['chorus_enabled'],
            chorus_base_delay=data['chorus_base_delay'],
            chorus_variation=data['chorus_variation'],
            chorus_period=data['chorus_period'],
            reverb_std_enabled=data['reverb_std_enabled'],
            unknown_0x4a5bbf90=data['unknown_0x4a5bbf90'],
            reverb_std_time=data['reverb_std_time'],
            reverb_std_pre_delay=data['reverb_std_pre_delay'],
            reverb_std_damping=data['reverb_std_damping'],
            reverb_std_coloration=data['reverb_std_coloration'],
            reverb_std_mix=data['reverb_std_mix'],
            delay_enabled=data['delay_enabled'],
            delay0=data['delay0'],
            delay1=data['delay1'],
            delay2=data['delay2'],
            delay_feedback0=data['delay_feedback0'],
            delay_feedback1=data['delay_feedback1'],
            delay_feedback2=data['delay_feedback2'],
            delay_output0=data['delay_output0'],
            delay_output1=data['delay_output1'],
            delay_output2=data['delay_output2'],
            unknown_0xcf45711c=data['unknown_0xcf45711c'],
            unknown_0x626d1e9b=data['unknown_0x626d1e9b'],
            unknown_0x7d8ee273=data['unknown_0x7d8ee273'],
            unknown_0x83378e6a=data['unknown_0x83378e6a'],
            unknown_0xf549d269=data['unknown_0xf549d269'],
            unknown_0x11fdae16=data['unknown_0x11fdae16'],
            unknown_0xa3c439c1=data['unknown_0xa3c439c1'],
            unknown_0x2dc70efe=data['unknown_0x2dc70efe'],
            unknown_0xe2bd3706=data['unknown_0xe2bd3706'],
            unknown_0x5e29cef8=data['unknown_0x5e29cef8'],
            unknown_0x35ae9f10=data['unknown_0x35ae9f10'],
            bitcrusher_enabled=data['bitcrusher_enabled'],
            unknown_0xf51a1d6a=data['unknown_0xf51a1d6a'],
            bitcrusher_gain=data['bitcrusher_gain'],
            bitcrusher_bit_depth=data['bitcrusher_bit_depth'],
            unknown_0x58096e0b=data['unknown_0x58096e0b'],
            phaser_enabled=data['phaser_enabled'],
            phaser_frequency=data['phaser_frequency'],
            phaser_feedback=data['phaser_feedback'],
            phaser_invert=data['phaser_invert'],
            phaser_mix=data['phaser_mix'],
            phaser_sweep=data['phaser_sweep'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'room_volume': self.room_volume,
            'priority': self.priority,
            'reverb_hi_enabled': self.reverb_hi_enabled,
            'unknown_0x3263c26e': self.unknown_0x3263c26e,
            'reverb_hi_time': self.reverb_hi_time,
            'reverb_hi_pre_delay': self.reverb_hi_pre_delay,
            'reverb_hi_damping': self.reverb_hi_damping,
            'reverb_hi_coloration': self.reverb_hi_coloration,
            'reverb_hi_cross_talk': self.reverb_hi_cross_talk,
            'reverb_hi_mix': self.reverb_hi_mix,
            'chorus_enabled': self.chorus_enabled,
            'chorus_base_delay': self.chorus_base_delay,
            'chorus_variation': self.chorus_variation,
            'chorus_period': self.chorus_period,
            'reverb_std_enabled': self.reverb_std_enabled,
            'unknown_0x4a5bbf90': self.unknown_0x4a5bbf90,
            'reverb_std_time': self.reverb_std_time,
            'reverb_std_pre_delay': self.reverb_std_pre_delay,
            'reverb_std_damping': self.reverb_std_damping,
            'reverb_std_coloration': self.reverb_std_coloration,
            'reverb_std_mix': self.reverb_std_mix,
            'delay_enabled': self.delay_enabled,
            'delay0': self.delay0,
            'delay1': self.delay1,
            'delay2': self.delay2,
            'delay_feedback0': self.delay_feedback0,
            'delay_feedback1': self.delay_feedback1,
            'delay_feedback2': self.delay_feedback2,
            'delay_output0': self.delay_output0,
            'delay_output1': self.delay_output1,
            'delay_output2': self.delay_output2,
            'unknown_0xcf45711c': self.unknown_0xcf45711c,
            'unknown_0x626d1e9b': self.unknown_0x626d1e9b,
            'unknown_0x7d8ee273': self.unknown_0x7d8ee273,
            'unknown_0x83378e6a': self.unknown_0x83378e6a,
            'unknown_0xf549d269': self.unknown_0xf549d269,
            'unknown_0x11fdae16': self.unknown_0x11fdae16,
            'unknown_0xa3c439c1': self.unknown_0xa3c439c1,
            'unknown_0x2dc70efe': self.unknown_0x2dc70efe,
            'unknown_0xe2bd3706': self.unknown_0xe2bd3706,
            'unknown_0x5e29cef8': self.unknown_0x5e29cef8,
            'unknown_0x35ae9f10': self.unknown_0x35ae9f10,
            'bitcrusher_enabled': self.bitcrusher_enabled,
            'unknown_0xf51a1d6a': self.unknown_0xf51a1d6a,
            'bitcrusher_gain': self.bitcrusher_gain,
            'bitcrusher_bit_depth': self.bitcrusher_bit_depth,
            'unknown_0x58096e0b': self.unknown_0x58096e0b,
            'phaser_enabled': self.phaser_enabled,
            'phaser_frequency': self.phaser_frequency,
            'phaser_feedback': self.phaser_feedback,
            'phaser_invert': self.phaser_invert,
            'phaser_mix': self.phaser_mix,
            'phaser_sweep': self.phaser_sweep,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_room_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_reverb_hi_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x3263c26e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_reverb_hi_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_hi_pre_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_hi_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_hi_coloration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_hi_cross_talk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_hi_mix(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chorus_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_chorus_base_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chorus_variation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chorus_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_std_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4a5bbf90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_reverb_std_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_std_pre_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_std_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_std_coloration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverb_std_mix(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_delay0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_feedback0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_feedback1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_feedback2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_output0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_output1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_delay_output2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xcf45711c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x626d1e9b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7d8ee273(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x83378e6a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf549d269(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11fdae16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa3c439c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2dc70efe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe2bd3706(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5e29cef8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x35ae9f10(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bitcrusher_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf51a1d6a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bitcrusher_gain(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bitcrusher_bit_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x58096e0b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phaser_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_phaser_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phaser_feedback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phaser_invert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phaser_mix(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phaser_sweep(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbd9ea266: ('room_volume', _decode_room_volume),
    0x86cf23f4: ('priority', _decode_priority),
    0xa00360cc: ('reverb_hi_enabled', _decode_reverb_hi_enabled),
    0x3263c26e: ('unknown_0x3263c26e', _decode_unknown_0x3263c26e),
    0xc5868061: ('reverb_hi_time', _decode_reverb_hi_time),
    0xc6f50032: ('reverb_hi_pre_delay', _decode_reverb_hi_pre_delay),
    0xcba5555d: ('reverb_hi_damping', _decode_reverb_hi_damping),
    0x7319cf50: ('reverb_hi_coloration', _decode_reverb_hi_coloration),
    0x3dc3f16f: ('reverb_hi_cross_talk', _decode_reverb_hi_cross_talk),
    0xd5518b6c: ('reverb_hi_mix', _decode_reverb_hi_mix),
    0x26997ccb: ('chorus_enabled', _decode_chorus_enabled),
    0x121bdfad: ('chorus_base_delay', _decode_chorus_base_delay),
    0xe8796bce: ('chorus_variation', _decode_chorus_variation),
    0x24bbd5e4: ('chorus_period', _decode_chorus_period),
    0xff31631b: ('reverb_std_enabled', _decode_reverb_std_enabled),
    0x4a5bbf90: ('unknown_0x4a5bbf90', _decode_unknown_0x4a5bbf90),
    0x9662498a: ('reverb_std_time', _decode_reverb_std_time),
    0x91855d62: ('reverb_std_pre_delay', _decode_reverb_std_pre_delay),
    0xd34d2029: ('reverb_std_damping', _decode_reverb_std_damping),
    0xdc78e83d: ('reverb_std_coloration', _decode_reverb_std_coloration),
    0x820b509e: ('reverb_std_mix', _decode_reverb_std_mix),
    0xe9a36031: ('delay_enabled', _decode_delay_enabled),
    0x62c49457: ('delay0', _decode_delay0),
    0xda78f332: ('delay1', _decode_delay1),
    0xc8cd5cdc: ('delay2', _decode_delay2),
    0x7c14ff17: ('delay_feedback0', _decode_delay_feedback0),
    0xc4a89872: ('delay_feedback1', _decode_delay_feedback1),
    0xd61d379c: ('delay_feedback2', _decode_delay_feedback2),
    0x9f75987f: ('delay_output0', _decode_delay_output0),
    0x27c9ff1a: ('delay_output1', _decode_delay_output1),
    0x357c50f4: ('delay_output2', _decode_delay_output2),
    0xcf45711c: ('unknown_0xcf45711c', _decode_unknown_0xcf45711c),
    0x626d1e9b: ('unknown_0x626d1e9b', _decode_unknown_0x626d1e9b),
    0x7d8ee273: ('unknown_0x7d8ee273', _decode_unknown_0x7d8ee273),
    0x83378e6a: ('unknown_0x83378e6a', _decode_unknown_0x83378e6a),
    0xf549d269: ('unknown_0xf549d269', _decode_unknown_0xf549d269),
    0x11fdae16: ('unknown_0x11fdae16', _decode_unknown_0x11fdae16),
    0xa3c439c1: ('unknown_0xa3c439c1', _decode_unknown_0xa3c439c1),
    0x2dc70efe: ('unknown_0x2dc70efe', _decode_unknown_0x2dc70efe),
    0xe2bd3706: ('unknown_0xe2bd3706', _decode_unknown_0xe2bd3706),
    0x5e29cef8: ('unknown_0x5e29cef8', _decode_unknown_0x5e29cef8),
    0x35ae9f10: ('unknown_0x35ae9f10', _decode_unknown_0x35ae9f10),
    0x3e8d8694: ('bitcrusher_enabled', _decode_bitcrusher_enabled),
    0xf51a1d6a: ('unknown_0xf51a1d6a', _decode_unknown_0xf51a1d6a),
    0xbb1a0f34: ('bitcrusher_gain', _decode_bitcrusher_gain),
    0xeb009039: ('bitcrusher_bit_depth', _decode_bitcrusher_bit_depth),
    0x58096e0b: ('unknown_0x58096e0b', _decode_unknown_0x58096e0b),
    0x3d8cad84: ('phaser_enabled', _decode_phaser_enabled),
    0x23c340f6: ('phaser_frequency', _decode_phaser_frequency),
    0x1e5a52b8: ('phaser_feedback', _decode_phaser_feedback),
    0x1d69bec4: ('phaser_invert', _decode_phaser_invert),
    0x24538c4a: ('phaser_mix', _decode_phaser_mix),
    0xd5388116: ('phaser_sweep', _decode_phaser_sweep),
}
