# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData


@dataclasses.dataclass()
class HyperModeData(BaseProperty):
    initial_time_max: float = dataclasses.field(default=15.0)
    initial_time_min: float = dataclasses.field(default=10.0)
    duration_max: float = dataclasses.field(default=25.0)
    duration_min: float = dataclasses.field(default=20.0)
    check_delay_max: float = dataclasses.field(default=25.0)
    check_delay_min: float = dataclasses.field(default=20.0)
    check_chance: float = dataclasses.field(default=100.0)
    shot: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xb1/\xda+')  # 0xb12fda2b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_time_max))

        data.write(b'WOu\xca')  # 0x574f75ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_time_min))

        data.write(b'\xcb\x83\xbfw')  # 0xcb83bf77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration_max))

        data.write(b'-\xe3\x10\x96')  # 0x2de31096
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration_min))

        data.write(b'\x0c%\x06\xbc')  # 0xc2506bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.check_delay_max))

        data.write(b'\xeaE\xa9]')  # 0xea45a95d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.check_delay_min))

        data.write(b'\x95\xc1\x9d\t')  # 0x95c19d09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.check_chance))

        data.write(b'U\xd8\x9a\xb7')  # 0x55d89ab7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shot.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_time_max=data['initial_time_max'],
            initial_time_min=data['initial_time_min'],
            duration_max=data['duration_max'],
            duration_min=data['duration_min'],
            check_delay_max=data['check_delay_max'],
            check_delay_min=data['check_delay_min'],
            check_chance=data['check_chance'],
            shot=LaunchProjectileData.from_json(data['shot']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'initial_time_max': self.initial_time_max,
            'initial_time_min': self.initial_time_min,
            'duration_max': self.duration_max,
            'duration_min': self.duration_min,
            'check_delay_max': self.check_delay_max,
            'check_delay_min': self.check_delay_min,
            'check_chance': self.check_chance,
            'shot': self.shot.to_json(),
            'vulnerability': self.vulnerability.to_json(),
        }


def _decode_initial_time_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_time_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_check_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_check_delay_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_check_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shot(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb12fda2b: ('initial_time_max', _decode_initial_time_max),
    0x574f75ca: ('initial_time_min', _decode_initial_time_min),
    0xcb83bf77: ('duration_max', _decode_duration_max),
    0x2de31096: ('duration_min', _decode_duration_min),
    0xc2506bc: ('check_delay_max', _decode_check_delay_max),
    0xea45a95d: ('check_delay_min', _decode_check_delay_min),
    0x95c19d09: ('check_chance', _decode_check_chance),
    0x55d89ab7: ('shot', _decode_shot),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
}
