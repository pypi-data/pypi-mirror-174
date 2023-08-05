# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class EmperorIngStage1TentacleData(BaseProperty):
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    normal_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    warp_attack_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    melee_attack_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    projectile_attack_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    stay_retracted_time: float = dataclasses.field(default=0.0)
    tentacle_damaged_sound: AssetId = dataclasses.field(default=0x0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')\xdfa\xe1')  # 0x29df61e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8dsx\xa4')  # 0x8d7378a4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.warp_attack_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ly\x05O')  # 0x6c79054f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_attack_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<-$\x92')  # 0x3c2d2492
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_attack_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'I\x1c&W')  # 0x491c2657
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stay_retracted_time))

        data.write(b'\xe1\x9fF\x08')  # 0xe19f4608
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.tentacle_damaged_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=HealthInfo.from_json(data['health']),
            normal_vulnerability=DamageVulnerability.from_json(data['normal_vulnerability']),
            warp_attack_vulnerability=DamageVulnerability.from_json(data['warp_attack_vulnerability']),
            melee_attack_vulnerability=DamageVulnerability.from_json(data['melee_attack_vulnerability']),
            projectile_attack_vulnerability=DamageVulnerability.from_json(data['projectile_attack_vulnerability']),
            stay_retracted_time=data['stay_retracted_time'],
            tentacle_damaged_sound=data['tentacle_damaged_sound'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health.to_json(),
            'normal_vulnerability': self.normal_vulnerability.to_json(),
            'warp_attack_vulnerability': self.warp_attack_vulnerability.to_json(),
            'melee_attack_vulnerability': self.melee_attack_vulnerability.to_json(),
            'projectile_attack_vulnerability': self.projectile_attack_vulnerability.to_json(),
            'stay_retracted_time': self.stay_retracted_time,
            'tentacle_damaged_sound': self.tentacle_damaged_sound,
        }


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_normal_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_warp_attack_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_melee_attack_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_projectile_attack_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_stay_retracted_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tentacle_damaged_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcf90d15e: ('health', _decode_health),
    0x29df61e1: ('normal_vulnerability', _decode_normal_vulnerability),
    0x8d7378a4: ('warp_attack_vulnerability', _decode_warp_attack_vulnerability),
    0x6c79054f: ('melee_attack_vulnerability', _decode_melee_attack_vulnerability),
    0x3c2d2492: ('projectile_attack_vulnerability', _decode_projectile_attack_vulnerability),
    0x491c2657: ('stay_retracted_time', _decode_stay_retracted_time),
    0xe19f4608: ('tentacle_damaged_sound', _decode_tentacle_damaged_sound),
}
