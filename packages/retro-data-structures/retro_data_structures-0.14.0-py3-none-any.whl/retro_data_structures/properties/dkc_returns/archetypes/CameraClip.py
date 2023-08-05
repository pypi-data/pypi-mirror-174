# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class CameraClip(BaseProperty):
    near_clip_plane: float = dataclasses.field(default=0.20000000298023224)
    far_clip_plane: float = dataclasses.field(default=750.0)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xf4\x81\x7f\x13')  # 0xf4817f13
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.near_clip_plane))

        data.write(b'\x84\xecJt')  # 0x84ec4a74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_clip_plane))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            near_clip_plane=data['near_clip_plane'],
            far_clip_plane=data['far_clip_plane'],
        )

    def to_json(self) -> dict:
        return {
            'near_clip_plane': self.near_clip_plane,
            'far_clip_plane': self.far_clip_plane,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf4817f13, 0x84ec4a74)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[CameraClip]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        return None

    return CameraClip(
        dec[2],
        dec[5],
    )


def _decode_near_clip_plane(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_clip_plane(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf4817f13: ('near_clip_plane', _decode_near_clip_plane),
    0x84ec4a74: ('far_clip_plane', _decode_far_clip_plane),
}
