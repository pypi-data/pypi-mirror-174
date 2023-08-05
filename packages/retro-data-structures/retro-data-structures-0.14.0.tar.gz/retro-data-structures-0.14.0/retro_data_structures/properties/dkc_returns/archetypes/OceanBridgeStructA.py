# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class OceanBridgeStructA(BaseProperty):
    model_select: enums.ModelSelect = dataclasses.field(default=enums.ModelSelect.Unknown1)

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

        data.write(b'W0\x049')  # 0x57300439
        data.write(b'\x00\x04')  # size
        self.model_select.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            model_select=enums.ModelSelect.from_json(data['model_select']),
        )

    def to_json(self) -> dict:
        return {
            'model_select': self.model_select.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x57300439)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[OceanBridgeStructA]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHL')

    dec = _FAST_FORMAT.unpack(data.read(10))
    if (dec[0]) != _FAST_IDS:
        return None

    return OceanBridgeStructA(
        enums.ModelSelect(dec[2]),
    )


def _decode_model_select(data: typing.BinaryIO, property_size: int):
    return enums.ModelSelect.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x57300439: ('model_select', _decode_model_select),
}
