# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class RumbleEffect(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_rumble: int = dataclasses.field(default=240)
    effect: enums.Effect = dataclasses.field(default=enums.Effect.Unknown1)
    unknown: Spline = dataclasses.field(default_factory=Spline)
    radius: float = dataclasses.field(default=20.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKCRETURNS

    @classmethod
    def object_type(cls) -> str:
        return 'RUMB'

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O\x7f\xec9')  # 0x4f7fec39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_rumble))

        data.write(b')]#\x8b')  # 0x295d238b
        data.write(b'\x00\x04')  # size
        self.effect.to_stream(data)

        data.write(b'\x05\xa4Q\xed')  # 0x5a451ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flags_rumble=data['flags_rumble'],
            effect=enums.Effect.from_json(data['effect']),
            unknown=Spline.from_json(data['unknown']),
            radius=data['radius'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_rumble': self.flags_rumble,
            'effect': self.effect.to_json(),
            'unknown': self.unknown.to_json(),
            'radius': self.radius,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_rumble(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_effect(data: typing.BinaryIO, property_size: int):
    return enums.Effect.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x4f7fec39: ('flags_rumble', _decode_flags_rumble),
    0x295d238b: ('effect', _decode_effect),
    0x5a451ed: ('unknown', _decode_unknown),
    0x78c507eb: ('radius', _decode_radius),
}
