# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.ShotParam import ShotParam


@dataclasses.dataclass()
class BeamInfo(BaseProperty):
    cooldown: float = dataclasses.field(default=0.0)
    normal_damage: ShotParam = dataclasses.field(default_factory=ShotParam)
    charged_damage: ShotParam = dataclasses.field(default_factory=ShotParam)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        cooldown = struct.unpack('>f', data.read(4))[0]
        normal_damage = ShotParam.from_stream(data, property_size)
        charged_damage = ShotParam.from_stream(data, property_size)
        return cls(cooldown, normal_damage, charged_damage)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>f', self.cooldown))
        self.normal_damage.to_stream(data)
        self.charged_damage.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cooldown=data['cooldown'],
            normal_damage=ShotParam.from_json(data['normal_damage']),
            charged_damage=ShotParam.from_json(data['charged_damage']),
        )

    def to_json(self) -> dict:
        return {
            'cooldown': self.cooldown,
            'normal_damage': self.normal_damage.to_json(),
            'charged_damage': self.charged_damage.to_json(),
        }
