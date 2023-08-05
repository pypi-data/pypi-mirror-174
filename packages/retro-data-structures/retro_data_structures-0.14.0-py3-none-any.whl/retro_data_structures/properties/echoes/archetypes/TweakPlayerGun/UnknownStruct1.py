# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    super_missile: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    darkburst: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    sunburst: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    sonic_boom: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)
    unknown: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xc7\x13\xac\xf9')  # 0xc713acf9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_missile.to_stream(data, default_override={'damage_amount': 180.0, 'radius_damage_amount': 120.0, 'damage_radius': 8.0, 'knock_back_power': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19F\x8f*')  # 0x19468f2a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.darkburst.to_stream(data, default_override={'weapon_type': 1, 'damage_amount': 150.0, 'radius_damage_amount': 150.0, 'damage_radius': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'H\xacm\xd8')  # 0x48ac6dd8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sunburst.to_stream(data, default_override={'weapon_type': 2, 'damage_amount': 300.0, 'radius_damage_amount': 150.0, 'damage_radius': 8.0, 'knock_back_power': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc1\xc3\x15\xff')  # 0xc1c315ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sonic_boom.to_stream(data, default_override={'weapon_type': 3, 'damage_amount': 1.2000000476837158, 'radius_damage_amount': 1.2000000476837158})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x88\\l')  # 0x42885c6c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data, default_override={'weapon_type': 8})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            super_missile=TDamageInfo.from_json(data['super_missile']),
            darkburst=TDamageInfo.from_json(data['darkburst']),
            sunburst=TDamageInfo.from_json(data['sunburst']),
            sonic_boom=TDamageInfo.from_json(data['sonic_boom']),
            unknown=TDamageInfo.from_json(data['unknown']),
        )

    def to_json(self) -> dict:
        return {
            'super_missile': self.super_missile.to_json(),
            'darkburst': self.darkburst.to_json(),
            'sunburst': self.sunburst.to_json(),
            'sonic_boom': self.sonic_boom.to_json(),
            'unknown': self.unknown.to_json(),
        }


def _decode_super_missile(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'damage_amount': 180.0, 'radius_damage_amount': 120.0, 'damage_radius': 8.0, 'knock_back_power': 8.0})


def _decode_darkburst(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 1, 'damage_amount': 150.0, 'radius_damage_amount': 150.0, 'damage_radius': 10.0})


def _decode_sunburst(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 2, 'damage_amount': 300.0, 'radius_damage_amount': 150.0, 'damage_radius': 8.0, 'knock_back_power': 8.0})


def _decode_sonic_boom(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 3, 'damage_amount': 1.2000000476837158, 'radius_damage_amount': 1.2000000476837158})


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 8})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc713acf9: ('super_missile', _decode_super_missile),
    0x19468f2a: ('darkburst', _decode_darkburst),
    0x48ac6dd8: ('sunburst', _decode_sunburst),
    0xc1c315ff: ('sonic_boom', _decode_sonic_boom),
    0x42885c6c: ('unknown', _decode_unknown),
}
