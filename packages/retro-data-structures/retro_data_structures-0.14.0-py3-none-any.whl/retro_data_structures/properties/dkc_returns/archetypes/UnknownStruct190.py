# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct190(BaseProperty):
    unknown: int = dataclasses.field(default=1)
    beam_duration: float = dataclasses.field(default=3.0)

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

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'GJ\x91\xdb')  # 0x474a91db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            beam_duration=data['beam_duration'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'beam_duration': self.beam_duration,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8a58a7f8, 0x474a91db)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct190]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHf')

    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        return None

    return UnknownStruct190(
        dec[2],
        dec[5],
    )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_beam_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown', _decode_unknown),
    0x474a91db: ('beam_duration', _decode_beam_duration),
}
