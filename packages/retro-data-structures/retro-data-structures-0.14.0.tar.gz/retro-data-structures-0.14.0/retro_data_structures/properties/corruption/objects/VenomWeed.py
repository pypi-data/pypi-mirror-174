# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId


@dataclasses.dataclass()
class VenomWeed(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    density: float = dataclasses.field(default=1.0)
    max_depth: float = dataclasses.field(default=0.0)
    location_variance: float = dataclasses.field(default=0.0)
    detection_radius: float = dataclasses.field(default=0.0)
    grab_radius: float = dataclasses.field(default=0.0)
    unknown_0xd50d757d: float = dataclasses.field(default=3.0)
    unknown_0xcc689024: float = dataclasses.field(default=2.5)
    unknown_0x723737bc: float = dataclasses.field(default=0.0)
    unknown_0x57452dd9: float = dataclasses.field(default=0.0)
    retreat_depth: float = dataclasses.field(default=0.0)
    move_speed: float = dataclasses.field(default=0.0)
    unknown_0x11f854e2: float = dataclasses.field(default=0.0)
    max_slope: float = dataclasses.field(default=0.0)
    min_size: float = dataclasses.field(default=0.0)
    max_size: float = dataclasses.field(default=0.0)
    height_offset: float = dataclasses.field(default=0.0)
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_looped: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    sound_into_ground: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    unknown_0xff90b1e5: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    unknown_0x4473fec0: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    retreat_particle_system: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    unknown_0x534c2bbf: int = dataclasses.field(default=0)
    unknown_0x8e30f547: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    unknown_0x12289828: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def object_type(cls) -> str:
        return 'WEED'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_VenomWeed.rso']

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
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
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

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'd\xe5\xfe\x9f')  # 0x64e5fe9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.density))

        data.write(b'#\xce\xf9_')  # 0x23cef95f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_depth))

        data.write(b'\xbe\x02\xe4V')  # 0xbe02e456
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.location_variance))

        data.write(b'!\xcd\xcf!')  # 0x21cdcf21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_radius))

        data.write(b'\x89fG#')  # 0x89664723
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_radius))

        data.write(b'\xd5\ru}')  # 0xd50d757d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd50d757d))

        data.write(b'\xcch\x90$')  # 0xcc689024
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcc689024))

        data.write(b'r77\xbc')  # 0x723737bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x723737bc))

        data.write(b'WE-\xd9')  # 0x57452dd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x57452dd9))

        data.write(b'\\ \xb0\xc7')  # 0x5c20b0c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.retreat_depth))

        data.write(b'd\x97\xc7P')  # 0x6497c750
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_speed))

        data.write(b'\x11\xf8T\xe2')  # 0x11f854e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11f854e2))

        data.write(b'\xa7U\xc1\xdf')  # 0xa755c1df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_slope))

        data.write(b'U\x8cm\xd7')  # 0x558c6dd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_size))

        data.write(b'\xc5\xff}=')  # 0xc5ff7d3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_size))

        data.write(b'\xb2\xeb\xc2:')  # 0xb2ebc23a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.height_offset))

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08\xbc\x9a\x8c')  # 0x8bc9a8c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_looped))

        data.write(b'm\r\xb9c')  # 0x6d0db963
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_into_ground))

        data.write(b'\xff\x90\xb1\xe5')  # 0xff90b1e5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xff90b1e5))

        data.write(b'Ds\xfe\xc0')  # 0x4473fec0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x4473fec0))

        data.write(b'\x81\xd5\xaek')  # 0x81d5ae6b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.retreat_particle_system))

        data.write(b'SL+\xbf')  # 0x534c2bbf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x534c2bbf))

        data.write(b'\x8e0\xf5G')  # 0x8e30f547
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x8e30f547))

        data.write(b'\x12(\x98(')  # 0x12289828
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x12289828))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            density=data['density'],
            max_depth=data['max_depth'],
            location_variance=data['location_variance'],
            detection_radius=data['detection_radius'],
            grab_radius=data['grab_radius'],
            unknown_0xd50d757d=data['unknown_0xd50d757d'],
            unknown_0xcc689024=data['unknown_0xcc689024'],
            unknown_0x723737bc=data['unknown_0x723737bc'],
            unknown_0x57452dd9=data['unknown_0x57452dd9'],
            retreat_depth=data['retreat_depth'],
            move_speed=data['move_speed'],
            unknown_0x11f854e2=data['unknown_0x11f854e2'],
            max_slope=data['max_slope'],
            min_size=data['min_size'],
            max_size=data['max_size'],
            height_offset=data['height_offset'],
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            sound_looped=data['sound_looped'],
            sound_into_ground=data['sound_into_ground'],
            unknown_0xff90b1e5=data['unknown_0xff90b1e5'],
            unknown_0x4473fec0=data['unknown_0x4473fec0'],
            retreat_particle_system=data['retreat_particle_system'],
            unknown_0x534c2bbf=data['unknown_0x534c2bbf'],
            unknown_0x8e30f547=data['unknown_0x8e30f547'],
            unknown_0x12289828=data['unknown_0x12289828'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'actor_information': self.actor_information.to_json(),
            'character_animation_information': self.character_animation_information.to_json(),
            'density': self.density,
            'max_depth': self.max_depth,
            'location_variance': self.location_variance,
            'detection_radius': self.detection_radius,
            'grab_radius': self.grab_radius,
            'unknown_0xd50d757d': self.unknown_0xd50d757d,
            'unknown_0xcc689024': self.unknown_0xcc689024,
            'unknown_0x723737bc': self.unknown_0x723737bc,
            'unknown_0x57452dd9': self.unknown_0x57452dd9,
            'retreat_depth': self.retreat_depth,
            'move_speed': self.move_speed,
            'unknown_0x11f854e2': self.unknown_0x11f854e2,
            'max_slope': self.max_slope,
            'min_size': self.min_size,
            'max_size': self.max_size,
            'height_offset': self.height_offset,
            'contact_damage': self.contact_damage.to_json(),
            'sound_looped': self.sound_looped,
            'sound_into_ground': self.sound_into_ground,
            'unknown_0xff90b1e5': self.unknown_0xff90b1e5,
            'unknown_0x4473fec0': self.unknown_0x4473fec0,
            'retreat_particle_system': self.retreat_particle_system,
            'unknown_0x534c2bbf': self.unknown_0x534c2bbf,
            'unknown_0x8e30f547': self.unknown_0x8e30f547,
            'unknown_0x12289828': self.unknown_0x12289828,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_density(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_location_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd50d757d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcc689024(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x723737bc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x57452dd9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_retreat_depth(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11f854e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_slope(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_height_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_sound_looped(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_into_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xff90b1e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x4473fec0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_retreat_particle_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x534c2bbf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8e30f547(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x12289828(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x64e5fe9f: ('density', _decode_density),
    0x23cef95f: ('max_depth', _decode_max_depth),
    0xbe02e456: ('location_variance', _decode_location_variance),
    0x21cdcf21: ('detection_radius', _decode_detection_radius),
    0x89664723: ('grab_radius', _decode_grab_radius),
    0xd50d757d: ('unknown_0xd50d757d', _decode_unknown_0xd50d757d),
    0xcc689024: ('unknown_0xcc689024', _decode_unknown_0xcc689024),
    0x723737bc: ('unknown_0x723737bc', _decode_unknown_0x723737bc),
    0x57452dd9: ('unknown_0x57452dd9', _decode_unknown_0x57452dd9),
    0x5c20b0c7: ('retreat_depth', _decode_retreat_depth),
    0x6497c750: ('move_speed', _decode_move_speed),
    0x11f854e2: ('unknown_0x11f854e2', _decode_unknown_0x11f854e2),
    0xa755c1df: ('max_slope', _decode_max_slope),
    0x558c6dd7: ('min_size', _decode_min_size),
    0xc5ff7d3d: ('max_size', _decode_max_size),
    0xb2ebc23a: ('height_offset', _decode_height_offset),
    0xd756416e: ('contact_damage', _decode_contact_damage),
    0x8bc9a8c: ('sound_looped', _decode_sound_looped),
    0x6d0db963: ('sound_into_ground', _decode_sound_into_ground),
    0xff90b1e5: ('unknown_0xff90b1e5', _decode_unknown_0xff90b1e5),
    0x4473fec0: ('unknown_0x4473fec0', _decode_unknown_0x4473fec0),
    0x81d5ae6b: ('retreat_particle_system', _decode_retreat_particle_system),
    0x534c2bbf: ('unknown_0x534c2bbf', _decode_unknown_0x534c2bbf),
    0x8e30f547: ('unknown_0x8e30f547', _decode_unknown_0x8e30f547),
    0x12289828: ('unknown_0x12289828', _decode_unknown_0x12289828),
}
