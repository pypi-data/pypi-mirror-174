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
class Brizgee(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    waypoint_approach_distance: float = dataclasses.field(default=2.5)
    wall_turn_speed: float = dataclasses.field(default=360.0)
    floor_turn_speed: float = dataclasses.field(default=720.0)
    down_turn_speed: float = dataclasses.field(default=120.0)
    visible_distance: float = dataclasses.field(default=40.0)
    forward_moving_priority: float = dataclasses.field(default=0.20000000298023224)
    no_shell_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    no_shell_skin: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=0xffffffff)
    shell_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    shell_health: float = dataclasses.field(default=2.0)
    shell_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown: float = dataclasses.field(default=1.5)
    poison_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    poison_time: float = dataclasses.field(default=2.0)
    shell_break_sound: AssetId = dataclasses.field(default=0x0)
    poison_hit_sound: AssetId = dataclasses.field(default=0x0)
    player_poison_sound: AssetId = dataclasses.field(default=0x0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'BRZG'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['WallCrawler.rel', 'Parasite.rel']

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
        data.write(b'\x00\x14')  # 20 properties

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
        self.patterned.to_stream(data)
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

        data.write(b's;\xd2|')  # 0x733bd27c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.waypoint_approach_distance))

        data.write(b'\xacG\xc6(')  # 0xac47c628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_turn_speed))

        data.write(b'\x8eO{)')  # 0x8e4f7b29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_turn_speed))

        data.write(b'=<\x1bv')  # 0x3d3c1b76
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.down_turn_speed))

        data.write(b'\xa7%0\xe8')  # 0xa72530e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_distance))

        data.write(b'^jT\xb8')  # 0x5e6a54b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_moving_priority))

        data.write(b'\x07\xf9G\xf4')  # 0x7f947f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.no_shell_model))

        data.write(b'\x0bs%\xea')  # 0xb7325ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.no_shell_skin))

        data.write(b'\xf5s\xe1\x1c')  # 0xf573e11c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shell_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaa\x13%:')  # 0xaa13253a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shell_health))

        data.write(b'\xb4\x82\xe5\xdd')  # 0xb482e5dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shell_contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x80\xda\x80S')  # 0x80da8053
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x14=\x18\xc6')  # 0x143d18c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.poison_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x89G\xd4')  # 0xf78947d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.poison_time))

        data.write(b'j\x94*`')  # 0x6a942a60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shell_break_sound))

        data.write(b'\x80\x83\x92\xec')  # 0x808392ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.poison_hit_sound))

        data.write(b'\xdf-\x80\x17')  # 0xdf2d8017
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.player_poison_sound))

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
            waypoint_approach_distance=data['waypoint_approach_distance'],
            wall_turn_speed=data['wall_turn_speed'],
            floor_turn_speed=data['floor_turn_speed'],
            down_turn_speed=data['down_turn_speed'],
            visible_distance=data['visible_distance'],
            forward_moving_priority=data['forward_moving_priority'],
            no_shell_model=data['no_shell_model'],
            no_shell_skin=data['no_shell_skin'],
            shell_vulnerability=DamageVulnerability.from_json(data['shell_vulnerability']),
            shell_health=data['shell_health'],
            shell_contact_damage=DamageInfo.from_json(data['shell_contact_damage']),
            unknown=data['unknown'],
            poison_damage=DamageInfo.from_json(data['poison_damage']),
            poison_time=data['poison_time'],
            shell_break_sound=data['shell_break_sound'],
            poison_hit_sound=data['poison_hit_sound'],
            player_poison_sound=data['player_poison_sound'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'wall_turn_speed': self.wall_turn_speed,
            'floor_turn_speed': self.floor_turn_speed,
            'down_turn_speed': self.down_turn_speed,
            'visible_distance': self.visible_distance,
            'forward_moving_priority': self.forward_moving_priority,
            'no_shell_model': self.no_shell_model,
            'no_shell_skin': self.no_shell_skin,
            'shell_vulnerability': self.shell_vulnerability.to_json(),
            'shell_health': self.shell_health,
            'shell_contact_damage': self.shell_contact_damage.to_json(),
            'unknown': self.unknown,
            'poison_damage': self.poison_damage.to_json(),
            'poison_time': self.poison_time,
            'shell_break_sound': self.shell_break_sound,
            'poison_hit_sound': self.poison_hit_sound,
            'player_poison_sound': self.player_poison_sound,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_down_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_moving_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_no_shell_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_no_shell_skin(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shell_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_shell_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_poison_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_poison_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shell_break_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_poison_hit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_player_poison_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0xac47c628: ('wall_turn_speed', _decode_wall_turn_speed),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0x3d3c1b76: ('down_turn_speed', _decode_down_turn_speed),
    0xa72530e8: ('visible_distance', _decode_visible_distance),
    0x5e6a54b8: ('forward_moving_priority', _decode_forward_moving_priority),
    0x7f947f4: ('no_shell_model', _decode_no_shell_model),
    0xb7325ea: ('no_shell_skin', _decode_no_shell_skin),
    0xf573e11c: ('shell_vulnerability', _decode_shell_vulnerability),
    0xaa13253a: ('shell_health', _decode_shell_health),
    0xb482e5dd: ('shell_contact_damage', _decode_shell_contact_damage),
    0x80da8053: ('unknown', _decode_unknown),
    0x143d18c6: ('poison_damage', _decode_poison_damage),
    0xf78947d4: ('poison_time', _decode_poison_time),
    0x6a942a60: ('shell_break_sound', _decode_shell_break_sound),
    0x808392ec: ('poison_hit_sound', _decode_poison_hit_sound),
    0xdf2d8017: ('player_poison_sound', _decode_player_poison_sound),
}
