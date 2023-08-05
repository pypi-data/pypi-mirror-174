# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class Misc(BaseProperty):
    unknown_0x8aacfc27: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    unknown_0xa054ff1c: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    imploder_annihilator: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    ai_burn_damage: float = dataclasses.field(default=0.25)
    unknown_0x4848f444: float = dataclasses.field(default=5.0)
    max_absorbed_phazon_shots: int = dataclasses.field(default=5)
    unknown_0x3ae5d1fa: float = dataclasses.field(default=0.75)

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

        data.write(b"\x8a\xac\xfc'")  # 0x8aacfc27
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x8aacfc27.to_stream(data, default_override={'weapon_type': 1, 'damage_amount': 1.0, 'radius_damage_amount': 1.0, 'damage_radius': 0.0, 'knock_back_power': 0.10000000149011612})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0T\xff\x1c')  # 0xa054ff1c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa054ff1c.to_stream(data, default_override={'weapon_type': 2, 'damage_amount': 0.800000011920929, 'radius_damage_amount': 0.800000011920929, 'damage_radius': 0.0, 'knock_back_power': 0.800000011920929})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab\xfa\x93\xe9')  # 0xabfa93e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.imploder_annihilator.to_stream(data, default_override={'weapon_type': 3, 'damage_amount': 0.800000011920929, 'radius_damage_amount': 0.800000011920929, 'damage_radius': 0.0, 'knock_back_power': 0.800000011920929})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xf9\xbf3')  # 0xf8f9bf33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ai_burn_damage))

        data.write(b'HH\xf4D')  # 0x4848f444
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4848f444))

        data.write(b'\x1eq\x02"')  # 0x1e710222
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_absorbed_phazon_shots))

        data.write(b':\xe5\xd1\xfa')  # 0x3ae5d1fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3ae5d1fa))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8aacfc27=TDamageInfo.from_json(data['unknown_0x8aacfc27']),
            unknown_0xa054ff1c=TDamageInfo.from_json(data['unknown_0xa054ff1c']),
            imploder_annihilator=TDamageInfo.from_json(data['imploder_annihilator']),
            ai_burn_damage=data['ai_burn_damage'],
            unknown_0x4848f444=data['unknown_0x4848f444'],
            max_absorbed_phazon_shots=data['max_absorbed_phazon_shots'],
            unknown_0x3ae5d1fa=data['unknown_0x3ae5d1fa'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8aacfc27': self.unknown_0x8aacfc27.to_json(),
            'unknown_0xa054ff1c': self.unknown_0xa054ff1c.to_json(),
            'imploder_annihilator': self.imploder_annihilator.to_json(),
            'ai_burn_damage': self.ai_burn_damage,
            'unknown_0x4848f444': self.unknown_0x4848f444,
            'max_absorbed_phazon_shots': self.max_absorbed_phazon_shots,
            'unknown_0x3ae5d1fa': self.unknown_0x3ae5d1fa,
        }


def _decode_unknown_0x8aacfc27(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 1, 'damage_amount': 1.0, 'radius_damage_amount': 1.0, 'damage_radius': 0.0, 'knock_back_power': 0.10000000149011612})


def _decode_unknown_0xa054ff1c(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 2, 'damage_amount': 0.800000011920929, 'radius_damage_amount': 0.800000011920929, 'damage_radius': 0.0, 'knock_back_power': 0.800000011920929})


def _decode_imploder_annihilator(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 3, 'damage_amount': 0.800000011920929, 'radius_damage_amount': 0.800000011920929, 'damage_radius': 0.0, 'knock_back_power': 0.800000011920929})


def _decode_ai_burn_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4848f444(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_absorbed_phazon_shots(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3ae5d1fa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8aacfc27: ('unknown_0x8aacfc27', _decode_unknown_0x8aacfc27),
    0xa054ff1c: ('unknown_0xa054ff1c', _decode_unknown_0xa054ff1c),
    0xabfa93e9: ('imploder_annihilator', _decode_imploder_annihilator),
    0xf8f9bf33: ('ai_burn_damage', _decode_ai_burn_damage),
    0x4848f444: ('unknown_0x4848f444', _decode_unknown_0x4848f444),
    0x1e710222: ('max_absorbed_phazon_shots', _decode_max_absorbed_phazon_shots),
    0x3ae5d1fa: ('unknown_0x3ae5d1fa', _decode_unknown_0x3ae5d1fa),
}
