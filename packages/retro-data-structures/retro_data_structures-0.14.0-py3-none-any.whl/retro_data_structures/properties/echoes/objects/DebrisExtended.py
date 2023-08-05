# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId
from retro_data_structures.properties.echoes.core.Color import Color
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class DebrisExtended(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    cone_spread: float = dataclasses.field(default=180.0)
    movement_direction: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.0))
    minimum_speed: float = dataclasses.field(default=5.0)
    maximum_speed: float = dataclasses.field(default=15.0)
    minimum_spin_speed: float = dataclasses.field(default=1.0)
    maximum_spin_speed: float = dataclasses.field(default=1.2000000476837158)
    minimum_life_time: float = dataclasses.field(default=2.0)
    maximum_life_time: float = dataclasses.field(default=3.0)
    disable_collision_time: float = dataclasses.field(default=0.0)
    fade_in_end_percentage: float = dataclasses.field(default=10.0)
    fade_out_start_percentage: float = dataclasses.field(default=80.0)
    start_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    end_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    scale_start_percentage: float = dataclasses.field(default=80.0)
    final_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    unknown_0x417f4a91: float = dataclasses.field(default=0.375)
    gravity: float = dataclasses.field(default=25.0)
    position_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    particle1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    bounce_sound: AssetId = dataclasses.field(default=0x0)
    max_bounce_sounds: int = dataclasses.field(default=1)
    unknown_0x76c79503: float = dataclasses.field(default=1.0)
    unknown_0x310dfac8: float = dataclasses.field(default=1.0)
    particle_system1_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    particle_system1_uses_global_translation: bool = dataclasses.field(default=False)
    particle_system1_wait_for_particles_to_die: bool = dataclasses.field(default=False)
    particle_system1_orientation: int = dataclasses.field(default=0)  # Choice
    particle2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    particle_system2_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    particle_system2_uses_global_translation: bool = dataclasses.field(default=False)
    particle_system2_wait_for_particles_to_die: bool = dataclasses.field(default=False)
    particle_system2_orientation: int = dataclasses.field(default=0)  # Choice
    death_particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    death_particle_system_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    death_particle_system_orientation: int = dataclasses.field(default=0)  # Choice
    is_collider: bool = dataclasses.field(default=True)
    is_shootable: bool = dataclasses.field(default=False)
    die_on_collision: bool = dataclasses.field(default=False)
    unknown_0xdcaa0f22: bool = dataclasses.field(default=False)
    unknown_0xbfd82a19: bool = dataclasses.field(default=False)
    unknown_0x723d42d6: bool = dataclasses.field(default=True)
    unknown_0x4edb1d0e: bool = dataclasses.field(default=False)
    disable_physics_threshold: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'DBR2'

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
        data.write(b'\x00.')  # 46 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8do\xc3\x91')  # 0x8d6fc391
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cone_spread))

        data.write(b'\x80u\xf8\xf8')  # 0x8075f8f8
        data.write(b'\x00\x0c')  # size
        self.movement_direction.to_stream(data)

        data.write(b'\x01\x85&>')  # 0x185263e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_speed))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'\x86>\xbbv')  # 0x863ebb76
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_spin_speed))

        data.write(b'\x95{]\xdd')  # 0x957b5ddd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_spin_speed))

        data.write(b'T\xa8\xc4\x81')  # 0x54a8c481
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_life_time))

        data.write(b'}\xd69\x99')  # 0x7dd63999
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_life_time))

        data.write(b'kW\x1b\xa5')  # 0x6b571ba5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_collision_time))

        data.write(b'P\x05\x1a\x17')  # 0x50051a17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_end_percentage))

        data.write(b'cS\xc4\t')  # 0x6353c409
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_start_percentage))

        data.write(b':V4\xd8')  # 0x3a5634d8
        data.write(b'\x00\x10')  # size
        self.start_color.to_stream(data)

        data.write(b'Z\xf5\x86}')  # 0x5af5867d
        data.write(b'\x00\x10')  # size
        self.end_color.to_stream(data)

        data.write(b'\x88n|\x9f')  # 0x886e7c9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scale_start_percentage))

        data.write(b'\x80\xc2*\n')  # 0x80c22a0a
        data.write(b'\x00\x0c')  # size
        self.final_scale.to_stream(data)

        data.write(b'A\x7fJ\x91')  # 0x417f4a91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x417f4a91))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xef\x90\xf0\x9d')  # 0xef90f09d
        data.write(b'\x00\x0c')  # size
        self.position_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model))

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'A\xddM@')  # 0x41dd4d40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle1))

        data.write(b'\x0b\xb3\xcc\xae')  # 0xbb3ccae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.bounce_sound))

        data.write(b'\x99\x12\x02\xc3')  # 0x991202c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_bounce_sounds))

        data.write(b'v\xc7\x95\x03')  # 0x76c79503
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76c79503))

        data.write(b'1\r\xfa\xc8')  # 0x310dfac8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x310dfac8))

        data.write(b'\x19\xa6\xf7\x1f')  # 0x19a6f71f
        data.write(b'\x00\x0c')  # size
        self.particle_system1_scale.to_stream(data)

        data.write(b';\x03\xa0\x1e')  # 0x3b03a01e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_translation))

        data.write(b';\xdd/\xed')  # 0x3bdd2fed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_wait_for_particles_to_die))

        data.write(b'3J4\xbb')  # 0x334a34bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle_system1_orientation))

        data.write(b'\xc7I?\xee')  # 0xc7493fee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle2))

        data.write(b'n8%\xef')  # 0x6e3825ef
        data.write(b'\x00\x0c')  # size
        self.particle_system2_scale.to_stream(data)

        data.write(b'\xc9TM\xe6')  # 0xc9544de6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system2_uses_global_translation))

        data.write(b'\xc9\x8a\xc2\x15')  # 0xc98ac215
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system2_wait_for_particles_to_die))

        data.write(b'\xd9\xcc\xe9\xd9')  # 0xd9cce9d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.particle_system2_orientation))

        data.write(b'\x97\x90B\xc8')  # 0x979042c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_particle))

        data.write(b'\xe9!L\xd8')  # 0xe9214cd8
        data.write(b'\x00\x0c')  # size
        self.death_particle_system_scale.to_stream(data)

        data.write(b'\x9d\xfa\xde\xe0')  # 0x9dfadee0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_particle_system_orientation))

        data.write(b',{\x18\xdd')  # 0x2c7b18dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_collider))

        data.write(b'\x8cs\xcb|')  # 0x8c73cb7c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_shootable))

        data.write(b'\r\x7f\xadU')  # 0xd7fad55
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.die_on_collision))

        data.write(b'\xdc\xaa\x0f"')  # 0xdcaa0f22
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xdcaa0f22))

        data.write(b'\xbf\xd8*\x19')  # 0xbfd82a19
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbfd82a19))

        data.write(b'r=B\xd6')  # 0x723d42d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x723d42d6))

        data.write(b'N\xdb\x1d\x0e')  # 0x4edb1d0e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4edb1d0e))

        data.write(b')_\x05\xb7')  # 0x295f05b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_physics_threshold))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            cone_spread=data['cone_spread'],
            movement_direction=Vector.from_json(data['movement_direction']),
            minimum_speed=data['minimum_speed'],
            maximum_speed=data['maximum_speed'],
            minimum_spin_speed=data['minimum_spin_speed'],
            maximum_spin_speed=data['maximum_spin_speed'],
            minimum_life_time=data['minimum_life_time'],
            maximum_life_time=data['maximum_life_time'],
            disable_collision_time=data['disable_collision_time'],
            fade_in_end_percentage=data['fade_in_end_percentage'],
            fade_out_start_percentage=data['fade_out_start_percentage'],
            start_color=Color.from_json(data['start_color']),
            end_color=Color.from_json(data['end_color']),
            scale_start_percentage=data['scale_start_percentage'],
            final_scale=Vector.from_json(data['final_scale']),
            unknown_0x417f4a91=data['unknown_0x417f4a91'],
            gravity=data['gravity'],
            position_offset=Vector.from_json(data['position_offset']),
            model=data['model'],
            actor_information=ActorParameters.from_json(data['actor_information']),
            particle1=data['particle1'],
            bounce_sound=data['bounce_sound'],
            max_bounce_sounds=data['max_bounce_sounds'],
            unknown_0x76c79503=data['unknown_0x76c79503'],
            unknown_0x310dfac8=data['unknown_0x310dfac8'],
            particle_system1_scale=Vector.from_json(data['particle_system1_scale']),
            particle_system1_uses_global_translation=data['particle_system1_uses_global_translation'],
            particle_system1_wait_for_particles_to_die=data['particle_system1_wait_for_particles_to_die'],
            particle_system1_orientation=data['particle_system1_orientation'],
            particle2=data['particle2'],
            particle_system2_scale=Vector.from_json(data['particle_system2_scale']),
            particle_system2_uses_global_translation=data['particle_system2_uses_global_translation'],
            particle_system2_wait_for_particles_to_die=data['particle_system2_wait_for_particles_to_die'],
            particle_system2_orientation=data['particle_system2_orientation'],
            death_particle=data['death_particle'],
            death_particle_system_scale=Vector.from_json(data['death_particle_system_scale']),
            death_particle_system_orientation=data['death_particle_system_orientation'],
            is_collider=data['is_collider'],
            is_shootable=data['is_shootable'],
            die_on_collision=data['die_on_collision'],
            unknown_0xdcaa0f22=data['unknown_0xdcaa0f22'],
            unknown_0xbfd82a19=data['unknown_0xbfd82a19'],
            unknown_0x723d42d6=data['unknown_0x723d42d6'],
            unknown_0x4edb1d0e=data['unknown_0x4edb1d0e'],
            disable_physics_threshold=data['disable_physics_threshold'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'cone_spread': self.cone_spread,
            'movement_direction': self.movement_direction.to_json(),
            'minimum_speed': self.minimum_speed,
            'maximum_speed': self.maximum_speed,
            'minimum_spin_speed': self.minimum_spin_speed,
            'maximum_spin_speed': self.maximum_spin_speed,
            'minimum_life_time': self.minimum_life_time,
            'maximum_life_time': self.maximum_life_time,
            'disable_collision_time': self.disable_collision_time,
            'fade_in_end_percentage': self.fade_in_end_percentage,
            'fade_out_start_percentage': self.fade_out_start_percentage,
            'start_color': self.start_color.to_json(),
            'end_color': self.end_color.to_json(),
            'scale_start_percentage': self.scale_start_percentage,
            'final_scale': self.final_scale.to_json(),
            'unknown_0x417f4a91': self.unknown_0x417f4a91,
            'gravity': self.gravity,
            'position_offset': self.position_offset.to_json(),
            'model': self.model,
            'actor_information': self.actor_information.to_json(),
            'particle1': self.particle1,
            'bounce_sound': self.bounce_sound,
            'max_bounce_sounds': self.max_bounce_sounds,
            'unknown_0x76c79503': self.unknown_0x76c79503,
            'unknown_0x310dfac8': self.unknown_0x310dfac8,
            'particle_system1_scale': self.particle_system1_scale.to_json(),
            'particle_system1_uses_global_translation': self.particle_system1_uses_global_translation,
            'particle_system1_wait_for_particles_to_die': self.particle_system1_wait_for_particles_to_die,
            'particle_system1_orientation': self.particle_system1_orientation,
            'particle2': self.particle2,
            'particle_system2_scale': self.particle_system2_scale.to_json(),
            'particle_system2_uses_global_translation': self.particle_system2_uses_global_translation,
            'particle_system2_wait_for_particles_to_die': self.particle_system2_wait_for_particles_to_die,
            'particle_system2_orientation': self.particle_system2_orientation,
            'death_particle': self.death_particle,
            'death_particle_system_scale': self.death_particle_system_scale.to_json(),
            'death_particle_system_orientation': self.death_particle_system_orientation,
            'is_collider': self.is_collider,
            'is_shootable': self.is_shootable,
            'die_on_collision': self.die_on_collision,
            'unknown_0xdcaa0f22': self.unknown_0xdcaa0f22,
            'unknown_0xbfd82a19': self.unknown_0xbfd82a19,
            'unknown_0x723d42d6': self.unknown_0x723d42d6,
            'unknown_0x4edb1d0e': self.unknown_0x4edb1d0e,
            'disable_physics_threshold': self.disable_physics_threshold,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_cone_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_direction(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_minimum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_spin_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_spin_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disable_collision_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_end_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scale_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x417f4a91(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_position_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_particle1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_max_bounce_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x76c79503(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x310dfac8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_particle_system1_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system1_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_particle2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_particle_system2_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system2_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system2_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system2_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_particle(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_particle_system_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_death_particle_system_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_is_collider(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_shootable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_die_on_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xdcaa0f22(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbfd82a19(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x723d42d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4edb1d0e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_physics_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x8d6fc391: ('cone_spread', _decode_cone_spread),
    0x8075f8f8: ('movement_direction', _decode_movement_direction),
    0x185263e: ('minimum_speed', _decode_minimum_speed),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0x863ebb76: ('minimum_spin_speed', _decode_minimum_spin_speed),
    0x957b5ddd: ('maximum_spin_speed', _decode_maximum_spin_speed),
    0x54a8c481: ('minimum_life_time', _decode_minimum_life_time),
    0x7dd63999: ('maximum_life_time', _decode_maximum_life_time),
    0x6b571ba5: ('disable_collision_time', _decode_disable_collision_time),
    0x50051a17: ('fade_in_end_percentage', _decode_fade_in_end_percentage),
    0x6353c409: ('fade_out_start_percentage', _decode_fade_out_start_percentage),
    0x3a5634d8: ('start_color', _decode_start_color),
    0x5af5867d: ('end_color', _decode_end_color),
    0x886e7c9f: ('scale_start_percentage', _decode_scale_start_percentage),
    0x80c22a0a: ('final_scale', _decode_final_scale),
    0x417f4a91: ('unknown_0x417f4a91', _decode_unknown_0x417f4a91),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xef90f09d: ('position_offset', _decode_position_offset),
    0xc27ffa8f: ('model', _decode_model),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x41dd4d40: ('particle1', _decode_particle1),
    0xbb3ccae: ('bounce_sound', _decode_bounce_sound),
    0x991202c3: ('max_bounce_sounds', _decode_max_bounce_sounds),
    0x76c79503: ('unknown_0x76c79503', _decode_unknown_0x76c79503),
    0x310dfac8: ('unknown_0x310dfac8', _decode_unknown_0x310dfac8),
    0x19a6f71f: ('particle_system1_scale', _decode_particle_system1_scale),
    0x3b03a01e: ('particle_system1_uses_global_translation', _decode_particle_system1_uses_global_translation),
    0x3bdd2fed: ('particle_system1_wait_for_particles_to_die', _decode_particle_system1_wait_for_particles_to_die),
    0x334a34bb: ('particle_system1_orientation', _decode_particle_system1_orientation),
    0xc7493fee: ('particle2', _decode_particle2),
    0x6e3825ef: ('particle_system2_scale', _decode_particle_system2_scale),
    0xc9544de6: ('particle_system2_uses_global_translation', _decode_particle_system2_uses_global_translation),
    0xc98ac215: ('particle_system2_wait_for_particles_to_die', _decode_particle_system2_wait_for_particles_to_die),
    0xd9cce9d9: ('particle_system2_orientation', _decode_particle_system2_orientation),
    0x979042c8: ('death_particle', _decode_death_particle),
    0xe9214cd8: ('death_particle_system_scale', _decode_death_particle_system_scale),
    0x9dfadee0: ('death_particle_system_orientation', _decode_death_particle_system_orientation),
    0x2c7b18dd: ('is_collider', _decode_is_collider),
    0x8c73cb7c: ('is_shootable', _decode_is_shootable),
    0xd7fad55: ('die_on_collision', _decode_die_on_collision),
    0xdcaa0f22: ('unknown_0xdcaa0f22', _decode_unknown_0xdcaa0f22),
    0xbfd82a19: ('unknown_0xbfd82a19', _decode_unknown_0xbfd82a19),
    0x723d42d6: ('unknown_0x723d42d6', _decode_unknown_0x723d42d6),
    0x4edb1d0e: ('unknown_0x4edb1d0e', _decode_unknown_0x4edb1d0e),
    0x295f05b7: ('disable_physics_threshold', _decode_disable_physics_threshold),
}
