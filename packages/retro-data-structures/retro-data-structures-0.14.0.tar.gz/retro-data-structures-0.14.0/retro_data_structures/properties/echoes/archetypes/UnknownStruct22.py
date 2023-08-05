# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class UnknownStruct22(BaseProperty):
    portal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    attack_tip: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    stab_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xecfab026: int = dataclasses.field(default=-1)
    unknown_0x94880277: int = dataclasses.field(default=-1)
    sound_0x1c3e84b6: AssetId = dataclasses.field(default=0x0)
    sound_0xa93f0198: AssetId = dataclasses.field(default=0x0)

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

        data.write(b'J|N\xc2')  # 0x4a7c4ec2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.portal_effect))

        data.write(b'\xf1\x0bn\xf6')  # 0xf10b6ef6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_tip.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x94`\x16\xa9')  # 0x946016a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stab_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\xfa\xb0&')  # 0xecfab026
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xecfab026))

        data.write(b'\x94\x88\x02w')  # 0x94880277
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x94880277))

        data.write(b'\x1c>\x84\xb6')  # 0x1c3e84b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_0x1c3e84b6))

        data.write(b'\xa9?\x01\x98')  # 0xa93f0198
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_0xa93f0198))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            portal_effect=data['portal_effect'],
            attack_tip=AnimationParameters.from_json(data['attack_tip']),
            stab_damage=DamageInfo.from_json(data['stab_damage']),
            unknown_0xecfab026=data['unknown_0xecfab026'],
            unknown_0x94880277=data['unknown_0x94880277'],
            sound_0x1c3e84b6=data['sound_0x1c3e84b6'],
            sound_0xa93f0198=data['sound_0xa93f0198'],
        )

    def to_json(self) -> dict:
        return {
            'portal_effect': self.portal_effect,
            'attack_tip': self.attack_tip.to_json(),
            'stab_damage': self.stab_damage.to_json(),
            'unknown_0xecfab026': self.unknown_0xecfab026,
            'unknown_0x94880277': self.unknown_0x94880277,
            'sound_0x1c3e84b6': self.sound_0x1c3e84b6,
            'sound_0xa93f0198': self.sound_0xa93f0198,
        }


def _decode_portal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_attack_tip(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_stab_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xecfab026(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x94880277(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x1c3e84b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0xa93f0198(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4a7c4ec2: ('portal_effect', _decode_portal_effect),
    0xf10b6ef6: ('attack_tip', _decode_attack_tip),
    0x946016a9: ('stab_damage', _decode_stab_damage),
    0xecfab026: ('unknown_0xecfab026', _decode_unknown_0xecfab026),
    0x94880277: ('unknown_0x94880277', _decode_unknown_0x94880277),
    0x1c3e84b6: ('sound_0x1c3e84b6', _decode_sound_0x1c3e84b6),
    0xa93f0198: ('sound_0xa93f0198', _decode_sound_0xa93f0198),
}
