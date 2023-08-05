# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.CommandData import CommandData
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ControlHint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    priority: int = dataclasses.field(default=10)
    timer: float = dataclasses.field(default=0.0)
    cancel_method: int = dataclasses.field(default=0)
    cancel_press_count: int = dataclasses.field(default=0)
    cancel_press_time: float = dataclasses.field(default=0.0)
    cancel_timer: float = dataclasses.field(default=0.0)
    cancel_velocity: float = dataclasses.field(default=0.009999999776482582)
    unknown: int = dataclasses.field(default=0)
    command1: CommandData = dataclasses.field(default_factory=CommandData)
    command2: CommandData = dataclasses.field(default_factory=CommandData)
    command3: CommandData = dataclasses.field(default_factory=CommandData)
    command4: CommandData = dataclasses.field(default_factory=CommandData)
    command5: CommandData = dataclasses.field(default_factory=CommandData)
    command6: CommandData = dataclasses.field(default_factory=CommandData)
    command7: CommandData = dataclasses.field(default_factory=CommandData)
    command8: CommandData = dataclasses.field(default_factory=CommandData)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def object_type(cls) -> str:
        return 'CTLH'

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\x87GU.')  # 0x8747552e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.timer))

        data.write(b'{\x16|@')  # 0x7b167c40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cancel_method))

        data.write(b'\xaa\x8d\x1a\xfe')  # 0xaa8d1afe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cancel_press_count))

        data.write(b'&v[\x82')  # 0x26765b82
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cancel_press_time))

        data.write(b'jE\xd9\xd0')  # 0x6a45d9d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cancel_timer))

        data.write(b'\xc4\x92\xfe\xdf')  # 0xc492fedf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cancel_velocity))

        data.write(b'\x9ax\xa8\xbb')  # 0x9a78a8bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xa0\x84\r\xd7')  # 0xa0840dd7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xd7\x1a\xdf'")  # 0xd71adf27
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L\xbf\x93H')  # 0x4cbf9348
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"8'z\xc7")  # 0x38277ac7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\x826\xa8')  # 0xa38236a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd4\x1c\xe4X')  # 0xd41ce458
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O\xb9\xa87')  # 0x4fb9a837
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=-7F')  # 0x3d2d3746
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command8.to_stream(data)
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
            priority=data['priority'],
            timer=data['timer'],
            cancel_method=data['cancel_method'],
            cancel_press_count=data['cancel_press_count'],
            cancel_press_time=data['cancel_press_time'],
            cancel_timer=data['cancel_timer'],
            cancel_velocity=data['cancel_velocity'],
            unknown=data['unknown'],
            command1=CommandData.from_json(data['command1']),
            command2=CommandData.from_json(data['command2']),
            command3=CommandData.from_json(data['command3']),
            command4=CommandData.from_json(data['command4']),
            command5=CommandData.from_json(data['command5']),
            command6=CommandData.from_json(data['command6']),
            command7=CommandData.from_json(data['command7']),
            command8=CommandData.from_json(data['command8']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'priority': self.priority,
            'timer': self.timer,
            'cancel_method': self.cancel_method,
            'cancel_press_count': self.cancel_press_count,
            'cancel_press_time': self.cancel_press_time,
            'cancel_timer': self.cancel_timer,
            'cancel_velocity': self.cancel_velocity,
            'unknown': self.unknown,
            'command1': self.command1.to_json(),
            'command2': self.command2.to_json(),
            'command3': self.command3.to_json(),
            'command4': self.command4.to_json(),
            'command5': self.command5.to_json(),
            'command6': self.command6.to_json(),
            'command7': self.command7.to_json(),
            'command8': self.command8.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cancel_method(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cancel_press_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cancel_press_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cancel_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cancel_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_command1(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command2(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command3(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command4(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command5(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command6(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command7(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


def _decode_command8(data: typing.BinaryIO, property_size: int):
    return CommandData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x42087650: ('priority', _decode_priority),
    0x8747552e: ('timer', _decode_timer),
    0x7b167c40: ('cancel_method', _decode_cancel_method),
    0xaa8d1afe: ('cancel_press_count', _decode_cancel_press_count),
    0x26765b82: ('cancel_press_time', _decode_cancel_press_time),
    0x6a45d9d0: ('cancel_timer', _decode_cancel_timer),
    0xc492fedf: ('cancel_velocity', _decode_cancel_velocity),
    0x9a78a8bb: ('unknown', _decode_unknown),
    0xa0840dd7: ('command1', _decode_command1),
    0xd71adf27: ('command2', _decode_command2),
    0x4cbf9348: ('command3', _decode_command3),
    0x38277ac7: ('command4', _decode_command4),
    0xa38236a8: ('command5', _decode_command5),
    0xd41ce458: ('command6', _decode_command6),
    0x4fb9a837: ('command7', _decode_command7),
    0x3d2d3746: ('command8', _decode_command8),
}
