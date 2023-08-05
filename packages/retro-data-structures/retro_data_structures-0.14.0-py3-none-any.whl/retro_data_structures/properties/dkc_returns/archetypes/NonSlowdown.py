# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.AreaPathStructA import AreaPathStructA


@dataclasses.dataclass()
class NonSlowdown(BaseProperty):
    path_shape: AreaPathStructA = dataclasses.field(default_factory=AreaPathStructA)

    @classmethod
    def game(cls) -> Game:
        return Game.DKCRETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        data.write(b'\x7f\xcdi\x08')  # 0x7fcd6908
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path_shape.to_stream(data, default_override={'curvature': enums.Curvature.Unknown4})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            path_shape=AreaPathStructA.from_json(data['path_shape']),
        )

    def to_json(self) -> dict:
        return {
            'path_shape': self.path_shape.to_json(),
        }


def _decode_path_shape(data: typing.BinaryIO, property_size: int):
    return AreaPathStructA.from_stream(data, property_size, default_override={'curvature': enums.Curvature.Unknown4})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fcd6908: ('path_shape', _decode_path_shape),
}
