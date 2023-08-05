# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.WallCrawlerData import WallCrawlerData


@dataclasses.dataclass()
class Parasite(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flavor: int = dataclasses.field(default=0)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    telegraph_distance: float = dataclasses.field(default=10.0)
    waypoint_approach_distance: float = dataclasses.field(default=2.5)
    wall_turn_speed: float = dataclasses.field(default=360.0)
    floor_turn_speed: float = dataclasses.field(default=180.0)
    down_turn_speed: float = dataclasses.field(default=120.0)
    stuck_time: float = dataclasses.field(default=0.20000000298023224)
    unknown_0xd5c25506: float = dataclasses.field(default=0.4000000059604645)
    behavior_influence_radius: float = dataclasses.field(default=6.0)
    separation_distance: float = dataclasses.field(default=2.5999999046325684)
    separation_priority: float = dataclasses.field(default=1.0)
    alignment_priority: float = dataclasses.field(default=0.800000011920929)
    unknown_0x61959f0d: float = dataclasses.field(default=0.699999988079071)
    path_following_priority: float = dataclasses.field(default=0.8999999761581421)
    forward_moving_priority: float = dataclasses.field(default=0.20000000298023224)
    player_avoidance_distance: float = dataclasses.field(default=1.2999999523162842)
    player_avoidance_priority: float = dataclasses.field(default=0.20000000298023224)
    parasite_visible_distance: float = dataclasses.field(default=40.0)
    initially_paused: bool = dataclasses.field(default=False)
    wall_crawler_properties: WallCrawlerData = dataclasses.field(default_factory=WallCrawlerData)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def object_type(cls) -> str:
        return 'PARA'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_Parasite.rso']

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbesrJ')  # 0xbe73724a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flavor))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'mass': 25.0, 'damage_wait_time': 3.0, 'collision_radius': 0.20000000298023224, 'speed': 3.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0})
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

        data.write(b'\x84X\xb0\x03')  # 0x8458b003
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.telegraph_distance))

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

        data.write(b'\x0e~6\x98')  # 0xe7e3698
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stuck_time))

        data.write(b'\xd5\xc2U\x06')  # 0xd5c25506
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd5c25506))

        data.write(b'(\x03a\xaa')  # 0x280361aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.behavior_influence_radius))

        data.write(b"\x01U\x9f'")  # 0x1559f27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_distance))

        data.write(b'\xd2\x93\xeb\xc4')  # 0xd293ebc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_priority))

        data.write(b'HA\xf1\xde')  # 0x4841f1de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alignment_priority))

        data.write(b'a\x95\x9f\r')  # 0x61959f0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61959f0d))

        data.write(b'\xae\x11\xf9u')  # 0xae11f975
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.path_following_priority))

        data.write(b'^jT\xb8')  # 0x5e6a54b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.forward_moving_priority))

        data.write(b'\x95j\x12H')  # 0x956a1248
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_avoidance_distance))

        data.write(b'F\xacf\xab')  # 0x46ac66ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_avoidance_priority))

        data.write(b'N\xee\xc7\x85')  # 0x4eeec785
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.parasite_visible_distance))

        data.write(b'\xc3\xccC\x7f')  # 0xc3cc437f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.initially_paused))

        data.write(b'\xb7\x18\xb81')  # 0xb718b831
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wall_crawler_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flavor=data['flavor'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            telegraph_distance=data['telegraph_distance'],
            waypoint_approach_distance=data['waypoint_approach_distance'],
            wall_turn_speed=data['wall_turn_speed'],
            floor_turn_speed=data['floor_turn_speed'],
            down_turn_speed=data['down_turn_speed'],
            stuck_time=data['stuck_time'],
            unknown_0xd5c25506=data['unknown_0xd5c25506'],
            behavior_influence_radius=data['behavior_influence_radius'],
            separation_distance=data['separation_distance'],
            separation_priority=data['separation_priority'],
            alignment_priority=data['alignment_priority'],
            unknown_0x61959f0d=data['unknown_0x61959f0d'],
            path_following_priority=data['path_following_priority'],
            forward_moving_priority=data['forward_moving_priority'],
            player_avoidance_distance=data['player_avoidance_distance'],
            player_avoidance_priority=data['player_avoidance_priority'],
            parasite_visible_distance=data['parasite_visible_distance'],
            initially_paused=data['initially_paused'],
            wall_crawler_properties=WallCrawlerData.from_json(data['wall_crawler_properties']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flavor': self.flavor,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'telegraph_distance': self.telegraph_distance,
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'wall_turn_speed': self.wall_turn_speed,
            'floor_turn_speed': self.floor_turn_speed,
            'down_turn_speed': self.down_turn_speed,
            'stuck_time': self.stuck_time,
            'unknown_0xd5c25506': self.unknown_0xd5c25506,
            'behavior_influence_radius': self.behavior_influence_radius,
            'separation_distance': self.separation_distance,
            'separation_priority': self.separation_priority,
            'alignment_priority': self.alignment_priority,
            'unknown_0x61959f0d': self.unknown_0x61959f0d,
            'path_following_priority': self.path_following_priority,
            'forward_moving_priority': self.forward_moving_priority,
            'player_avoidance_distance': self.player_avoidance_distance,
            'player_avoidance_priority': self.player_avoidance_priority,
            'parasite_visible_distance': self.parasite_visible_distance,
            'initially_paused': self.initially_paused,
            'wall_crawler_properties': self.wall_crawler_properties.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flavor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 25.0, 'damage_wait_time': 3.0, 'collision_radius': 0.20000000298023224, 'speed': 3.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_telegraph_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_down_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stuck_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd5c25506(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_behavior_influence_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alignment_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61959f0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_path_following_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_forward_moving_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_avoidance_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_avoidance_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_parasite_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initially_paused(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wall_crawler_properties(data: typing.BinaryIO, property_size: int):
    return WallCrawlerData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbe73724a: ('flavor', _decode_flavor),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x8458b003: ('telegraph_distance', _decode_telegraph_distance),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0xac47c628: ('wall_turn_speed', _decode_wall_turn_speed),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0x3d3c1b76: ('down_turn_speed', _decode_down_turn_speed),
    0xe7e3698: ('stuck_time', _decode_stuck_time),
    0xd5c25506: ('unknown_0xd5c25506', _decode_unknown_0xd5c25506),
    0x280361aa: ('behavior_influence_radius', _decode_behavior_influence_radius),
    0x1559f27: ('separation_distance', _decode_separation_distance),
    0xd293ebc4: ('separation_priority', _decode_separation_priority),
    0x4841f1de: ('alignment_priority', _decode_alignment_priority),
    0x61959f0d: ('unknown_0x61959f0d', _decode_unknown_0x61959f0d),
    0xae11f975: ('path_following_priority', _decode_path_following_priority),
    0x5e6a54b8: ('forward_moving_priority', _decode_forward_moving_priority),
    0x956a1248: ('player_avoidance_distance', _decode_player_avoidance_distance),
    0x46ac66ab: ('player_avoidance_priority', _decode_player_avoidance_priority),
    0x4eeec785: ('parasite_visible_distance', _decode_parasite_visible_distance),
    0xc3cc437f: ('initially_paused', _decode_initially_paused),
    0xb718b831: ('wall_crawler_properties', _decode_wall_crawler_properties),
}
