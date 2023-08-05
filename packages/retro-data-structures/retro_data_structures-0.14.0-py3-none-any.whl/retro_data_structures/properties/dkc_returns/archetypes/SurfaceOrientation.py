# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SurfaceOrientation(BaseProperty):
    flags_surface_orientation: int = dataclasses.field(default=256)

    @classmethod
    def game(cls) -> Game:
        return Game.DKCRETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x10\xe6\xf3f')  # 0x10e6f366
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_surface_orientation))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_surface_orientation=data['flags_surface_orientation'],
        )

    def to_json(self) -> dict:
        return {
            'flags_surface_orientation': self.flags_surface_orientation,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x10e6f366)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SurfaceOrientation]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHl')

    dec = _FAST_FORMAT.unpack(data.read(10))
    if (dec[0]) != _FAST_IDS:
        return None

    return SurfaceOrientation(
        dec[2],
    )


def _decode_flags_surface_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x10e6f366: ('flags_surface_orientation', _decode_flags_surface_orientation),
}
