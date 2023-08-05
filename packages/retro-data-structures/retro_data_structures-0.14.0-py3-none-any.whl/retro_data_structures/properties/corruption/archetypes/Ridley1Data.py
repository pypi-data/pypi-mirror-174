# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo


@dataclasses.dataclass()
class Ridley1Data(BaseProperty):
    unknown_0xa0460b5e: float = dataclasses.field(default=90.0)
    unknown_0xf33b0dd4: float = dataclasses.field(default=65.0)
    unknown_0xa59260dd: float = dataclasses.field(default=60.0)
    unknown_0x5bbdbc45: float = dataclasses.field(default=35.0)
    unknown_0xbc1564b9: float = dataclasses.field(default=1000.0)
    damage_info_0xe82166db: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    below_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xf616d87b: float = dataclasses.field(default=15.0)
    below_bite_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x54031e21: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xb5194095: float = dataclasses.field(default=15.0)
    in_hand_bite_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xddd0212a: float = dataclasses.field(default=15.0)
    damage_info_0x6bb8e35c: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xf4c13980: float = dataclasses.field(default=15.0)
    in_hand_slap_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xa4cb7b3c: float = dataclasses.field(default=15.0)
    damage_info_0x742287f5: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xbe3b8e93: float = dataclasses.field(default=15.0)
    damage_info_0x78f4a916: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x76f0f23b: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x77edd892: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    above_missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    above_fireball_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x4fa2bce1: float = dataclasses.field(default=8.0)

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'\xa0F\x0b^')  # 0xa0460b5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa0460b5e))

        data.write(b'\xf3;\r\xd4')  # 0xf33b0dd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf33b0dd4))

        data.write(b'\xa5\x92`\xdd')  # 0xa59260dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa59260dd))

        data.write(b'[\xbd\xbcE')  # 0x5bbdbc45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5bbdbc45))

        data.write(b'\xbc\x15d\xb9')  # 0xbc1564b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbc1564b9))

        data.write(b'\xe8!f\xdb')  # 0xe82166db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xe82166db.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'60{\x98')  # 0x36307b98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.below_beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\x16\xd8{')  # 0xf616d87b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf616d87b))

        data.write(b'\xfa\xb0\x19\x9e')  # 0xfab0199e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.below_bite_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\x03\x1e!')  # 0x54031e21
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x54031e21.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb5\x19@\x95')  # 0xb5194095
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb5194095))

        data.write(b'\xd5Y\x17\xa9')  # 0xd55917a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.in_hand_bite_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\xd0!*')  # 0xddd0212a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xddd0212a))

        data.write(b'k\xb8\xe3\\')  # 0x6bb8e35c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x6bb8e35c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xc19\x80')  # 0xf4c13980
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf4c13980))

        data.write(b'G\xd4B~')  # 0x47d4427e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.in_hand_slap_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xcb{<')  # 0xa4cb7b3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa4cb7b3c))

        data.write(b't"\x87\xf5')  # 0x742287f5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x742287f5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbe;\x8e\x93')  # 0xbe3b8e93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbe3b8e93))

        data.write(b'x\xf4\xa9\x16')  # 0x78f4a916
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x78f4a916.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xf0\xf2;')  # 0x76f0f23b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x76f0f23b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w\xed\xd8\x92')  # 0x77edd892
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x77edd892.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xc79\xd2')  # 0xb6c739d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.above_missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y5\n\xc0')  # 0x79350ac0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.above_fireball_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O\xa2\xbc\xe1')  # 0x4fa2bce1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4fa2bce1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xa0460b5e=data['unknown_0xa0460b5e'],
            unknown_0xf33b0dd4=data['unknown_0xf33b0dd4'],
            unknown_0xa59260dd=data['unknown_0xa59260dd'],
            unknown_0x5bbdbc45=data['unknown_0x5bbdbc45'],
            unknown_0xbc1564b9=data['unknown_0xbc1564b9'],
            damage_info_0xe82166db=DamageInfo.from_json(data['damage_info_0xe82166db']),
            below_beam_damage=DamageInfo.from_json(data['below_beam_damage']),
            unknown_0xf616d87b=data['unknown_0xf616d87b'],
            below_bite_damage=DamageInfo.from_json(data['below_bite_damage']),
            damage_info_0x54031e21=DamageInfo.from_json(data['damage_info_0x54031e21']),
            unknown_0xb5194095=data['unknown_0xb5194095'],
            in_hand_bite_damage=DamageInfo.from_json(data['in_hand_bite_damage']),
            unknown_0xddd0212a=data['unknown_0xddd0212a'],
            damage_info_0x6bb8e35c=DamageInfo.from_json(data['damage_info_0x6bb8e35c']),
            unknown_0xf4c13980=data['unknown_0xf4c13980'],
            in_hand_slap_damage=DamageInfo.from_json(data['in_hand_slap_damage']),
            unknown_0xa4cb7b3c=data['unknown_0xa4cb7b3c'],
            damage_info_0x742287f5=DamageInfo.from_json(data['damage_info_0x742287f5']),
            unknown_0xbe3b8e93=data['unknown_0xbe3b8e93'],
            damage_info_0x78f4a916=DamageInfo.from_json(data['damage_info_0x78f4a916']),
            damage_info_0x76f0f23b=DamageInfo.from_json(data['damage_info_0x76f0f23b']),
            damage_info_0x77edd892=DamageInfo.from_json(data['damage_info_0x77edd892']),
            above_missile_damage=DamageInfo.from_json(data['above_missile_damage']),
            above_fireball_damage=DamageInfo.from_json(data['above_fireball_damage']),
            unknown_0x4fa2bce1=data['unknown_0x4fa2bce1'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xa0460b5e': self.unknown_0xa0460b5e,
            'unknown_0xf33b0dd4': self.unknown_0xf33b0dd4,
            'unknown_0xa59260dd': self.unknown_0xa59260dd,
            'unknown_0x5bbdbc45': self.unknown_0x5bbdbc45,
            'unknown_0xbc1564b9': self.unknown_0xbc1564b9,
            'damage_info_0xe82166db': self.damage_info_0xe82166db.to_json(),
            'below_beam_damage': self.below_beam_damage.to_json(),
            'unknown_0xf616d87b': self.unknown_0xf616d87b,
            'below_bite_damage': self.below_bite_damage.to_json(),
            'damage_info_0x54031e21': self.damage_info_0x54031e21.to_json(),
            'unknown_0xb5194095': self.unknown_0xb5194095,
            'in_hand_bite_damage': self.in_hand_bite_damage.to_json(),
            'unknown_0xddd0212a': self.unknown_0xddd0212a,
            'damage_info_0x6bb8e35c': self.damage_info_0x6bb8e35c.to_json(),
            'unknown_0xf4c13980': self.unknown_0xf4c13980,
            'in_hand_slap_damage': self.in_hand_slap_damage.to_json(),
            'unknown_0xa4cb7b3c': self.unknown_0xa4cb7b3c,
            'damage_info_0x742287f5': self.damage_info_0x742287f5.to_json(),
            'unknown_0xbe3b8e93': self.unknown_0xbe3b8e93,
            'damage_info_0x78f4a916': self.damage_info_0x78f4a916.to_json(),
            'damage_info_0x76f0f23b': self.damage_info_0x76f0f23b.to_json(),
            'damage_info_0x77edd892': self.damage_info_0x77edd892.to_json(),
            'above_missile_damage': self.above_missile_damage.to_json(),
            'above_fireball_damage': self.above_fireball_damage.to_json(),
            'unknown_0x4fa2bce1': self.unknown_0x4fa2bce1,
        }


def _decode_unknown_0xa0460b5e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf33b0dd4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa59260dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5bbdbc45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbc1564b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0xe82166db(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_below_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xf616d87b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_below_bite_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x54031e21(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xb5194095(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_in_hand_bite_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xddd0212a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0x6bb8e35c(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xf4c13980(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_in_hand_slap_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xa4cb7b3c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0x742287f5(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xbe3b8e93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0x78f4a916(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x76f0f23b(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x77edd892(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_above_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_above_fireball_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x4fa2bce1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa0460b5e: ('unknown_0xa0460b5e', _decode_unknown_0xa0460b5e),
    0xf33b0dd4: ('unknown_0xf33b0dd4', _decode_unknown_0xf33b0dd4),
    0xa59260dd: ('unknown_0xa59260dd', _decode_unknown_0xa59260dd),
    0x5bbdbc45: ('unknown_0x5bbdbc45', _decode_unknown_0x5bbdbc45),
    0xbc1564b9: ('unknown_0xbc1564b9', _decode_unknown_0xbc1564b9),
    0xe82166db: ('damage_info_0xe82166db', _decode_damage_info_0xe82166db),
    0x36307b98: ('below_beam_damage', _decode_below_beam_damage),
    0xf616d87b: ('unknown_0xf616d87b', _decode_unknown_0xf616d87b),
    0xfab0199e: ('below_bite_damage', _decode_below_bite_damage),
    0x54031e21: ('damage_info_0x54031e21', _decode_damage_info_0x54031e21),
    0xb5194095: ('unknown_0xb5194095', _decode_unknown_0xb5194095),
    0xd55917a9: ('in_hand_bite_damage', _decode_in_hand_bite_damage),
    0xddd0212a: ('unknown_0xddd0212a', _decode_unknown_0xddd0212a),
    0x6bb8e35c: ('damage_info_0x6bb8e35c', _decode_damage_info_0x6bb8e35c),
    0xf4c13980: ('unknown_0xf4c13980', _decode_unknown_0xf4c13980),
    0x47d4427e: ('in_hand_slap_damage', _decode_in_hand_slap_damage),
    0xa4cb7b3c: ('unknown_0xa4cb7b3c', _decode_unknown_0xa4cb7b3c),
    0x742287f5: ('damage_info_0x742287f5', _decode_damage_info_0x742287f5),
    0xbe3b8e93: ('unknown_0xbe3b8e93', _decode_unknown_0xbe3b8e93),
    0x78f4a916: ('damage_info_0x78f4a916', _decode_damage_info_0x78f4a916),
    0x76f0f23b: ('damage_info_0x76f0f23b', _decode_damage_info_0x76f0f23b),
    0x77edd892: ('damage_info_0x77edd892', _decode_damage_info_0x77edd892),
    0xb6c739d2: ('above_missile_damage', _decode_above_missile_damage),
    0x79350ac0: ('above_fireball_damage', _decode_above_fireball_damage),
    0x4fa2bce1: ('unknown_0x4fa2bce1', _decode_unknown_0x4fa2bce1),
}
