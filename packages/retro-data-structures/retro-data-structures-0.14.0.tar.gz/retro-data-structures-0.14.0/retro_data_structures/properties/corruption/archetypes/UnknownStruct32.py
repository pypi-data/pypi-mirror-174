# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct32(BaseProperty):
    initial_morph_time: float = dataclasses.field(default=15.0)
    rundas_to_ghor: float = dataclasses.field(default=80.0)
    rundas_to_gandrayda: float = dataclasses.field(default=20.0)
    unknown_0x8e975bd2: float = dataclasses.field(default=0.0)
    unknown_0xf848fa88: float = dataclasses.field(default=80.0)
    ghor_to_gandrayda: float = dataclasses.field(default=20.0)
    ghor_to_swarm: float = dataclasses.field(default=80.0)
    unknown_0x9fa5117d: float = dataclasses.field(default=0.0)
    unknown_0xc98d5dff: float = dataclasses.field(default=80.0)
    gandrayda_to_ghor: float = dataclasses.field(default=20.0)
    gandrayda_to_rundas: float = dataclasses.field(default=20.0)
    gandrayda_to_swarm: float = dataclasses.field(default=20.0)
    unknown_0xcbbd9a4e: float = dataclasses.field(default=20.0)
    unknown_0x106d3edb: float = dataclasses.field(default=20.0)
    unknown_0xa2675081: float = dataclasses.field(default=20.0)
    unknown_0x413aee5b: float = dataclasses.field(default=30.0)
    swarm_to_rundas: float = dataclasses.field(default=80.0)
    swarm_to_gandrayda: float = dataclasses.field(default=20.0)
    unknown_0x73ac8586: float = dataclasses.field(default=80.0)
    unknown_0x704c4fc6: float = dataclasses.field(default=0.0)
    unknown_0xc0597dc2: float = dataclasses.field(default=40.0)
    unknown_0x4b605ddb: float = dataclasses.field(default=40.0)
    unknown_0x931ea2ea: float = dataclasses.field(default=20.0)
    unknown_0x7a11bb7b: float = dataclasses.field(default=80.0)
    unknown_0xb4089be1: float = dataclasses.field(default=0.0)
    unknown_0x118f6e87: float = dataclasses.field(default=15.0)
    unknown_0x68737a67: float = dataclasses.field(default=85.0)
    unknown_0xa771b575: float = dataclasses.field(default=50.0)
    unknown_0x672a5c88: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'E\x16\x11\t')  # 0x45161109
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_morph_time))

        data.write(b'\xd2l\x1c\xad')  # 0xd26c1cad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rundas_to_ghor))

        data.write(b'Q\xb2\x85\xb8')  # 0x51b285b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rundas_to_gandrayda))

        data.write(b'\x8e\x97[\xd2')  # 0x8e975bd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8e975bd2))

        data.write(b'\xf8H\xfa\x88')  # 0xf848fa88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf848fa88))

        data.write(b'\x82K\x86a')  # 0x824b8661
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ghor_to_gandrayda))

        data.write(b'\xab~\x85\xa0')  # 0xab7e85a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ghor_to_swarm))

        data.write(b'\x9f\xa5\x11}')  # 0x9fa5117d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9fa5117d))

        data.write(b'\xc9\x8d]\xff')  # 0xc98d5dff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc98d5dff))

        data.write(b'\x99\x91\x1b\x85')  # 0x99911b85
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gandrayda_to_ghor))

        data.write(b'\x9fo\xe5s')  # 0x9f6fe573
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gandrayda_to_rundas))

        data.write(b'\x8d|a\x03')  # 0x8d7c6103
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gandrayda_to_swarm))

        data.write(b'\xcb\xbd\x9aN')  # 0xcbbd9a4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcbbd9a4e))

        data.write(b'\x10m>\xdb')  # 0x106d3edb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x106d3edb))

        data.write(b'\xa2gP\x81')  # 0xa2675081
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa2675081))

        data.write(b'A:\xee[')  # 0x413aee5b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x413aee5b))

        data.write(b'l\t\x1a\xaf')  # 0x6c091aaf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swarm_to_rundas))

        data.write(b' #Z1')  # 0x20235a31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swarm_to_gandrayda))

        data.write(b's\xac\x85\x86')  # 0x73ac8586
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x73ac8586))

        data.write(b'pLO\xc6')  # 0x704c4fc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x704c4fc6))

        data.write(b'\xc0Y}\xc2')  # 0xc0597dc2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc0597dc2))

        data.write(b'K`]\xdb')  # 0x4b605ddb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4b605ddb))

        data.write(b'\x93\x1e\xa2\xea')  # 0x931ea2ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x931ea2ea))

        data.write(b'z\x11\xbb{')  # 0x7a11bb7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7a11bb7b))

        data.write(b'\xb4\x08\x9b\xe1')  # 0xb4089be1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb4089be1))

        data.write(b'\x11\x8fn\x87')  # 0x118f6e87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x118f6e87))

        data.write(b'hszg')  # 0x68737a67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x68737a67))

        data.write(b'\xa7q\xb5u')  # 0xa771b575
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa771b575))

        data.write(b'g*\\\x88')  # 0x672a5c88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x672a5c88))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_morph_time=data['initial_morph_time'],
            rundas_to_ghor=data['rundas_to_ghor'],
            rundas_to_gandrayda=data['rundas_to_gandrayda'],
            unknown_0x8e975bd2=data['unknown_0x8e975bd2'],
            unknown_0xf848fa88=data['unknown_0xf848fa88'],
            ghor_to_gandrayda=data['ghor_to_gandrayda'],
            ghor_to_swarm=data['ghor_to_swarm'],
            unknown_0x9fa5117d=data['unknown_0x9fa5117d'],
            unknown_0xc98d5dff=data['unknown_0xc98d5dff'],
            gandrayda_to_ghor=data['gandrayda_to_ghor'],
            gandrayda_to_rundas=data['gandrayda_to_rundas'],
            gandrayda_to_swarm=data['gandrayda_to_swarm'],
            unknown_0xcbbd9a4e=data['unknown_0xcbbd9a4e'],
            unknown_0x106d3edb=data['unknown_0x106d3edb'],
            unknown_0xa2675081=data['unknown_0xa2675081'],
            unknown_0x413aee5b=data['unknown_0x413aee5b'],
            swarm_to_rundas=data['swarm_to_rundas'],
            swarm_to_gandrayda=data['swarm_to_gandrayda'],
            unknown_0x73ac8586=data['unknown_0x73ac8586'],
            unknown_0x704c4fc6=data['unknown_0x704c4fc6'],
            unknown_0xc0597dc2=data['unknown_0xc0597dc2'],
            unknown_0x4b605ddb=data['unknown_0x4b605ddb'],
            unknown_0x931ea2ea=data['unknown_0x931ea2ea'],
            unknown_0x7a11bb7b=data['unknown_0x7a11bb7b'],
            unknown_0xb4089be1=data['unknown_0xb4089be1'],
            unknown_0x118f6e87=data['unknown_0x118f6e87'],
            unknown_0x68737a67=data['unknown_0x68737a67'],
            unknown_0xa771b575=data['unknown_0xa771b575'],
            unknown_0x672a5c88=data['unknown_0x672a5c88'],
        )

    def to_json(self) -> dict:
        return {
            'initial_morph_time': self.initial_morph_time,
            'rundas_to_ghor': self.rundas_to_ghor,
            'rundas_to_gandrayda': self.rundas_to_gandrayda,
            'unknown_0x8e975bd2': self.unknown_0x8e975bd2,
            'unknown_0xf848fa88': self.unknown_0xf848fa88,
            'ghor_to_gandrayda': self.ghor_to_gandrayda,
            'ghor_to_swarm': self.ghor_to_swarm,
            'unknown_0x9fa5117d': self.unknown_0x9fa5117d,
            'unknown_0xc98d5dff': self.unknown_0xc98d5dff,
            'gandrayda_to_ghor': self.gandrayda_to_ghor,
            'gandrayda_to_rundas': self.gandrayda_to_rundas,
            'gandrayda_to_swarm': self.gandrayda_to_swarm,
            'unknown_0xcbbd9a4e': self.unknown_0xcbbd9a4e,
            'unknown_0x106d3edb': self.unknown_0x106d3edb,
            'unknown_0xa2675081': self.unknown_0xa2675081,
            'unknown_0x413aee5b': self.unknown_0x413aee5b,
            'swarm_to_rundas': self.swarm_to_rundas,
            'swarm_to_gandrayda': self.swarm_to_gandrayda,
            'unknown_0x73ac8586': self.unknown_0x73ac8586,
            'unknown_0x704c4fc6': self.unknown_0x704c4fc6,
            'unknown_0xc0597dc2': self.unknown_0xc0597dc2,
            'unknown_0x4b605ddb': self.unknown_0x4b605ddb,
            'unknown_0x931ea2ea': self.unknown_0x931ea2ea,
            'unknown_0x7a11bb7b': self.unknown_0x7a11bb7b,
            'unknown_0xb4089be1': self.unknown_0xb4089be1,
            'unknown_0x118f6e87': self.unknown_0x118f6e87,
            'unknown_0x68737a67': self.unknown_0x68737a67,
            'unknown_0xa771b575': self.unknown_0xa771b575,
            'unknown_0x672a5c88': self.unknown_0x672a5c88,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x45161109, 0xd26c1cad, 0x51b285b8, 0x8e975bd2, 0xf848fa88, 0x824b8661, 0xab7e85a0, 0x9fa5117d, 0xc98d5dff, 0x99911b85, 0x9f6fe573, 0x8d7c6103, 0xcbbd9a4e, 0x106d3edb, 0xa2675081, 0x413aee5b, 0x6c091aaf, 0x20235a31, 0x73ac8586, 0x704c4fc6, 0xc0597dc2, 0x4b605ddb, 0x931ea2ea, 0x7a11bb7b, 0xb4089be1, 0x118f6e87, 0x68737a67, 0xa771b575, 0x672a5c88)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct32]:
    if property_count != 29:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    dec = _FAST_FORMAT.unpack(data.read(290))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72], dec[75], dec[78], dec[81], dec[84]) != _FAST_IDS:
        return None

    return UnknownStruct32(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
        dec[50],
        dec[53],
        dec[56],
        dec[59],
        dec[62],
        dec[65],
        dec[68],
        dec[71],
        dec[74],
        dec[77],
        dec[80],
        dec[83],
        dec[86],
    )


def _decode_initial_morph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rundas_to_ghor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rundas_to_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8e975bd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf848fa88(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ghor_to_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ghor_to_swarm(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9fa5117d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc98d5dff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gandrayda_to_ghor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gandrayda_to_rundas(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gandrayda_to_swarm(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcbbd9a4e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x106d3edb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa2675081(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x413aee5b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swarm_to_rundas(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swarm_to_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73ac8586(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x704c4fc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc0597dc2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4b605ddb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x931ea2ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7a11bb7b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb4089be1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x118f6e87(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x68737a67(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa771b575(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x672a5c88(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45161109: ('initial_morph_time', _decode_initial_morph_time),
    0xd26c1cad: ('rundas_to_ghor', _decode_rundas_to_ghor),
    0x51b285b8: ('rundas_to_gandrayda', _decode_rundas_to_gandrayda),
    0x8e975bd2: ('unknown_0x8e975bd2', _decode_unknown_0x8e975bd2),
    0xf848fa88: ('unknown_0xf848fa88', _decode_unknown_0xf848fa88),
    0x824b8661: ('ghor_to_gandrayda', _decode_ghor_to_gandrayda),
    0xab7e85a0: ('ghor_to_swarm', _decode_ghor_to_swarm),
    0x9fa5117d: ('unknown_0x9fa5117d', _decode_unknown_0x9fa5117d),
    0xc98d5dff: ('unknown_0xc98d5dff', _decode_unknown_0xc98d5dff),
    0x99911b85: ('gandrayda_to_ghor', _decode_gandrayda_to_ghor),
    0x9f6fe573: ('gandrayda_to_rundas', _decode_gandrayda_to_rundas),
    0x8d7c6103: ('gandrayda_to_swarm', _decode_gandrayda_to_swarm),
    0xcbbd9a4e: ('unknown_0xcbbd9a4e', _decode_unknown_0xcbbd9a4e),
    0x106d3edb: ('unknown_0x106d3edb', _decode_unknown_0x106d3edb),
    0xa2675081: ('unknown_0xa2675081', _decode_unknown_0xa2675081),
    0x413aee5b: ('unknown_0x413aee5b', _decode_unknown_0x413aee5b),
    0x6c091aaf: ('swarm_to_rundas', _decode_swarm_to_rundas),
    0x20235a31: ('swarm_to_gandrayda', _decode_swarm_to_gandrayda),
    0x73ac8586: ('unknown_0x73ac8586', _decode_unknown_0x73ac8586),
    0x704c4fc6: ('unknown_0x704c4fc6', _decode_unknown_0x704c4fc6),
    0xc0597dc2: ('unknown_0xc0597dc2', _decode_unknown_0xc0597dc2),
    0x4b605ddb: ('unknown_0x4b605ddb', _decode_unknown_0x4b605ddb),
    0x931ea2ea: ('unknown_0x931ea2ea', _decode_unknown_0x931ea2ea),
    0x7a11bb7b: ('unknown_0x7a11bb7b', _decode_unknown_0x7a11bb7b),
    0xb4089be1: ('unknown_0xb4089be1', _decode_unknown_0xb4089be1),
    0x118f6e87: ('unknown_0x118f6e87', _decode_unknown_0x118f6e87),
    0x68737a67: ('unknown_0x68737a67', _decode_unknown_0x68737a67),
    0xa771b575: ('unknown_0xa771b575', _decode_unknown_0xa771b575),
    0x672a5c88: ('unknown_0x672a5c88', _decode_unknown_0x672a5c88),
}
