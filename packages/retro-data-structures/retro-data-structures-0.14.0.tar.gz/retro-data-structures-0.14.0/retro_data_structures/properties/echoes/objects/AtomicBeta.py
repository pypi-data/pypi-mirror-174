# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class AtomicBeta(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    beam_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC', 'WPSC']}, default=0xffffffff)
    beam: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    contact_fx: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    beam_fade_time: float = dataclasses.field(default=1.0)
    beam_radius: float = dataclasses.field(default=0.10000000149011612)
    hover_speed: float = dataclasses.field(default=3.0)
    frozen_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    normal_rotate_speed: float = dataclasses.field(default=1.5)
    charging_rotate_speed: float = dataclasses.field(default=5.0)
    speed_change_rate: float = dataclasses.field(default=1.0)
    sound_0x14038b71: AssetId = dataclasses.field(default=0x0)
    sound_0x16a435cb: AssetId = dataclasses.field(default=0x0)
    sound_0x67edefc2: AssetId = dataclasses.field(default=0x0)
    damage_delay: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'ATMB'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['AtomicBeta.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'mass': 25.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_height_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0, 'damage_wait_time': 1.0, 'collision_radius': 0.5, 'collision_height': 1.5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05C\x9a\x08')  # 0x5439a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.beam_effect))

        data.write(b',\xbf\x98\x9b')  # 0x2cbf989b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.beam))

        data.write(b'\x13\xe3\x0eM')  # 0x13e30e4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2q\xea\xf5')  # 0xc271eaf5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.contact_fx))

        data.write(b'\x18\t?\xa8')  # 0x18093fa8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_fade_time))

        data.write(b'\xcb\n\xf0u')  # 0xcb0af075
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.beam_radius))

        data.write(b'\x84^\xf4\x89')  # 0x845ef489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_speed))

        data.write(b'A\x198\xaa')  # 0x411938aa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.frozen_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xce\x18\x93\xcc')  # 0xce1893cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.normal_rotate_speed))

        data.write(b'jE=\x89')  # 0x6a453d89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charging_rotate_speed))

        data.write(b'\xac *]')  # 0xac202a5d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed_change_rate))

        data.write(b'\x14\x03\x8bq')  # 0x14038b71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_0x14038b71))

        data.write(b'\x16\xa45\xcb')  # 0x16a435cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_0x16a435cb))

        data.write(b'g\xed\xef\xc2')  # 0x67edefc2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sound_0x67edefc2))

        data.write(b'\x8fO\xb7\x9d')  # 0x8f4fb79d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_delay))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            beam_effect=data['beam_effect'],
            beam=data['beam'],
            beam_damage=DamageInfo.from_json(data['beam_damage']),
            contact_fx=data['contact_fx'],
            beam_fade_time=data['beam_fade_time'],
            beam_radius=data['beam_radius'],
            hover_speed=data['hover_speed'],
            frozen_vulnerability=DamageVulnerability.from_json(data['frozen_vulnerability']),
            normal_rotate_speed=data['normal_rotate_speed'],
            charging_rotate_speed=data['charging_rotate_speed'],
            speed_change_rate=data['speed_change_rate'],
            sound_0x14038b71=data['sound_0x14038b71'],
            sound_0x16a435cb=data['sound_0x16a435cb'],
            sound_0x67edefc2=data['sound_0x67edefc2'],
            damage_delay=data['damage_delay'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'beam_effect': self.beam_effect,
            'beam': self.beam,
            'beam_damage': self.beam_damage.to_json(),
            'contact_fx': self.contact_fx,
            'beam_fade_time': self.beam_fade_time,
            'beam_radius': self.beam_radius,
            'hover_speed': self.hover_speed,
            'frozen_vulnerability': self.frozen_vulnerability.to_json(),
            'normal_rotate_speed': self.normal_rotate_speed,
            'charging_rotate_speed': self.charging_rotate_speed,
            'speed_change_rate': self.speed_change_rate,
            'sound_0x14038b71': self.sound_0x14038b71,
            'sound_0x16a435cb': self.sound_0x16a435cb,
            'sound_0x67edefc2': self.sound_0x67edefc2,
            'damage_delay': self.damage_delay,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 25.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_height_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0, 'damage_wait_time': 1.0, 'collision_radius': 0.5, 'collision_height': 1.5})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_beam_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_contact_fx(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_beam_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_beam_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_frozen_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_normal_rotate_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charging_rotate_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed_change_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_0x14038b71(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0x16a435cb(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0x67edefc2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x5439a08: ('beam_effect', _decode_beam_effect),
    0x2cbf989b: ('beam', _decode_beam),
    0x13e30e4d: ('beam_damage', _decode_beam_damage),
    0xc271eaf5: ('contact_fx', _decode_contact_fx),
    0x18093fa8: ('beam_fade_time', _decode_beam_fade_time),
    0xcb0af075: ('beam_radius', _decode_beam_radius),
    0x845ef489: ('hover_speed', _decode_hover_speed),
    0x411938aa: ('frozen_vulnerability', _decode_frozen_vulnerability),
    0xce1893cc: ('normal_rotate_speed', _decode_normal_rotate_speed),
    0x6a453d89: ('charging_rotate_speed', _decode_charging_rotate_speed),
    0xac202a5d: ('speed_change_rate', _decode_speed_change_rate),
    0x14038b71: ('sound_0x14038b71', _decode_sound_0x14038b71),
    0x16a435cb: ('sound_0x16a435cb', _decode_sound_0x16a435cb),
    0x67edefc2: ('sound_0x67edefc2', _decode_sound_0x67edefc2),
    0x8f4fb79d: ('damage_delay', _decode_damage_delay),
}
