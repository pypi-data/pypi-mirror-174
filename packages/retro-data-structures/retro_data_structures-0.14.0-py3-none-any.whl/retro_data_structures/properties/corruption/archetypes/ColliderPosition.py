# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.Convergence import Convergence


@dataclasses.dataclass()
class ColliderPosition(BaseProperty):
    collider_position_type: enums.ColliderPositionType = dataclasses.field(default=enums.ColliderPositionType.Unknown1)
    distance: float = dataclasses.field(default=5.0)
    backwards_distance: float = dataclasses.field(default=10.0)
    z_offset: float = dataclasses.field(default=2.7360000610351562)
    distance_convergence: Convergence = dataclasses.field(default_factory=Convergence)
    centroid_convergence: Convergence = dataclasses.field(default_factory=Convergence)
    camera_convergence: Convergence = dataclasses.field(default_factory=Convergence)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xe2\xaeG\x0c')  # 0xe2ae470c
        data.write(b'\x00\x04')  # size
        self.collider_position_type.to_stream(data)

        data.write(b'\xc3\xbfC\xbe')  # 0xc3bf43be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance))

        data.write(b'\xe7V+\xee')  # 0xe7562bee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.backwards_distance))

        data.write(b'\x803\xf9\xa3')  # 0x8033f9a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.z_offset))

        data.write(b'\xb1\x1d\x9e\x90')  # 0xb11d9e90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.distance_convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\xd4\x9ca')  # 0x81d49c61
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.centroid_convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xb1\x1f\x91')  # 0x51b11f91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.camera_convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            collider_position_type=enums.ColliderPositionType.from_json(data['collider_position_type']),
            distance=data['distance'],
            backwards_distance=data['backwards_distance'],
            z_offset=data['z_offset'],
            distance_convergence=Convergence.from_json(data['distance_convergence']),
            centroid_convergence=Convergence.from_json(data['centroid_convergence']),
            camera_convergence=Convergence.from_json(data['camera_convergence']),
        )

    def to_json(self) -> dict:
        return {
            'collider_position_type': self.collider_position_type.to_json(),
            'distance': self.distance,
            'backwards_distance': self.backwards_distance,
            'z_offset': self.z_offset,
            'distance_convergence': self.distance_convergence.to_json(),
            'centroid_convergence': self.centroid_convergence.to_json(),
            'camera_convergence': self.camera_convergence.to_json(),
        }


def _decode_collider_position_type(data: typing.BinaryIO, property_size: int):
    return enums.ColliderPositionType.from_stream(data)


def _decode_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_backwards_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_z_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_centroid_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_camera_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe2ae470c: ('collider_position_type', _decode_collider_position_type),
    0xc3bf43be: ('distance', _decode_distance),
    0xe7562bee: ('backwards_distance', _decode_backwards_distance),
    0x8033f9a3: ('z_offset', _decode_z_offset),
    0xb11d9e90: ('distance_convergence', _decode_distance_convergence),
    0x81d49c61: ('centroid_convergence', _decode_centroid_convergence),
    0x51b11f91: ('camera_convergence', _decode_camera_convergence),
}
