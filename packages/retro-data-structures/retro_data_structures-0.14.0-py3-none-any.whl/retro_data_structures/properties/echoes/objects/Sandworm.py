# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.archetypes.SandwormStruct import SandwormStruct
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class Sandworm(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0x06dee4c5: int = dataclasses.field(default=0)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    pincer_scale: float = dataclasses.field(default=1.0)
    walk_sound: AssetId = dataclasses.field(default=0x0)
    walk_vocal_sound: AssetId = dataclasses.field(default=0x0)
    melee_attack_sound: AssetId = dataclasses.field(default=0x0)
    eye_killed_sound: AssetId = dataclasses.field(default=0x0)
    pincer_l: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    pincer_r: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    unknown_0x63dcbbb6: float = dataclasses.field(default=9.0)
    unknown_0x2393c3c0: float = dataclasses.field(default=25.0)
    spit_attack_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    unknown_0x61f75902: float = dataclasses.field(default=60.0)
    charge_range_min: float = dataclasses.field(default=25.0)
    charge_range_max: float = dataclasses.field(default=30.0)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=0xffffffff)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    charge_impulse_horizontal: float = dataclasses.field(default=50.0)
    charge_impulse_vertical: float = dataclasses.field(default=50.0)
    unknown_0x2b053901: float = dataclasses.field(default=50.0)
    unknown_0x47e969d3: float = dataclasses.field(default=50.0)
    melee_impulse_horizontal: float = dataclasses.field(default=30.0)
    melee_impulse_vertical: float = dataclasses.field(default=15.0)
    morphball_toss_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    pincer_swipe_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xe593f1c6: float = dataclasses.field(default=25.0)
    unknown_0x3c5d53a4: float = dataclasses.field(default=2.0)
    unknown_0xda3dfc45: float = dataclasses.field(default=5.0)
    pursuit_frustration_timer: float = dataclasses.field(default=6.0)
    pursuit_frustration_radius: float = dataclasses.field(default=20.0)
    can_link_transfer: bool = dataclasses.field(default=False)
    eye_glow: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    part_0x3221407e: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    part_0x8b2a15ee: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    part_0x526c6956: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    part_0xd24a1751: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=0xffffffff)
    ing_boss_bomb_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x3d58f51f: float = dataclasses.field(default=0.0)
    bomb_bounce_sound: AssetId = dataclasses.field(default=0x0)
    bomb_explode_sound: AssetId = dataclasses.field(default=0x0)
    unknown_0x547f9400: float = dataclasses.field(default=50.0)
    unknown_0xefef7b45: float = dataclasses.field(default=10.0)
    sandworm_struct_0xb8c15f15: SandwormStruct = dataclasses.field(default_factory=SandwormStruct)
    sandworm_struct_0xce246628: SandwormStruct = dataclasses.field(default_factory=SandwormStruct)
    sandworm_struct_0x55578cfc: SandwormStruct = dataclasses.field(default_factory=SandwormStruct)
    sandworm_struct_0x23ee1452: SandwormStruct = dataclasses.field(default_factory=SandwormStruct)
    sandworm_struct_0xb89dfe86: SandwormStruct = dataclasses.field(default_factory=SandwormStruct)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'WORM'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Sandworm.rel']

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
        data.write(b'\x002')  # 50 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xde\xe4\xc5')  # 0x6dee4c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x06dee4c5))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'detection_range': 32.0, 'collision_radius': 0.5, 'collision_height': 1.0, 'creature_size': 2})
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

        data.write(b'=\xb5\x83\xae')  # 0x3db583ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pincer_scale))

        data.write(b'\xa2Cv\xec')  # 0xa24376ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.walk_sound))

        data.write(b'\xd3^\xb6\x9d')  # 0xd35eb69d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.walk_vocal_sound))

        data.write(b'\xaa\xda\xab\xb8')  # 0xaadaabb8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.melee_attack_sound))

        data.write(b'\x81(\xceJ')  # 0x8128ce4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.eye_killed_sound))

        data.write(b'f\xe3J\x08')  # 0x66e34a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.pincer_l))

        data.write(b'_?)\xe3')  # 0x5f3f29e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.pincer_r))

        data.write(b'c\xdc\xbb\xb6')  # 0x63dcbbb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x63dcbbb6))

        data.write(b'#\x93\xc3\xc0')  # 0x2393c3c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2393c3c0))

        data.write(b'\xf9F\x9eI')  # 0xf9469e49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.spit_attack_visor_effect))

        data.write(b'a\xf7Y\x02')  # 0x61f75902
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61f75902))

        data.write(b'*tF\xee')  # 0x2a7446ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_range_min))

        data.write(b'\xcc\x14\xe9\x0f')  # 0xcc14e90f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_range_max))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\t\r\xa8')  # 0x12090da8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_impulse_horizontal))

        data.write(b'\xc0{\xbe\x9a')  # 0xc07bbe9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_impulse_vertical))

        data.write(b'+\x059\x01')  # 0x2b053901
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2b053901))

        data.write(b'G\xe9i\xd3')  # 0x47e969d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x47e969d3))

        data.write(b'\xb8\xee\xcc\x95')  # 0xb8eecc95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_impulse_horizontal))

        data.write(b'\xf5\x9a\xf0\x1a')  # 0xf59af01a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_impulse_vertical))

        data.write(b'\xf8\xfdh\x85')  # 0xf8fd6885
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.morphball_toss_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D\x923\xbc')  # 0x449233bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pincer_swipe_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x93\xf1\xc6')  # 0xe593f1c6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe593f1c6))

        data.write(b'<]S\xa4')  # 0x3c5d53a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3c5d53a4))

        data.write(b'\xda=\xfcE')  # 0xda3dfc45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xda3dfc45))

        data.write(b'\xdf\xa4n\x80')  # 0xdfa46e80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pursuit_frustration_timer))

        data.write(b'I\xf3j?')  # 0x49f36a3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pursuit_frustration_radius))

        data.write(b'\xb4}\xd1\x8f')  # 0xb47dd18f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_link_transfer))

        data.write(b'\x0c\xa8-<')  # 0xca82d3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.eye_glow))

        data.write(b'2!@~')  # 0x3221407e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x3221407e))

        data.write(b'\x8b*\x15\xee')  # 0x8b2a15ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x8b2a15ee))

        data.write(b'RliV')  # 0x526c6956
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x526c6956))

        data.write(b'\xd2J\x17Q')  # 0xd24a1751
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xd24a1751))

        data.write(b'Da\xa8\xad')  # 0x4461a8ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_boss_bomb_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=X\xf5\x1f')  # 0x3d58f51f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3d58f51f))

        data.write(b'\x8cA\x06l')  # 0x8c41066c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.bomb_bounce_sound))

        data.write(b'\x86I\xfeS')  # 0x8649fe53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.bomb_explode_sound))

        data.write(b'T\x7f\x94\x00')  # 0x547f9400
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x547f9400))

        data.write(b'\xef\xef{E')  # 0xefef7b45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xefef7b45))

        data.write(b'\xb8\xc1_\x15')  # 0xb8c15f15
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sandworm_struct_0xb8c15f15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xce$f(')  # 0xce246628
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sandworm_struct_0xce246628.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'UW\x8c\xfc')  # 0x55578cfc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sandworm_struct_0x55578cfc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\xee\x14R')  # 0x23ee1452
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sandworm_struct_0x23ee1452.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\x9d\xfe\x86')  # 0xb89dfe86
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sandworm_struct_0xb89dfe86.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
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
            unknown_0x06dee4c5=data['unknown_0x06dee4c5'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            pincer_scale=data['pincer_scale'],
            walk_sound=data['walk_sound'],
            walk_vocal_sound=data['walk_vocal_sound'],
            melee_attack_sound=data['melee_attack_sound'],
            eye_killed_sound=data['eye_killed_sound'],
            pincer_l=data['pincer_l'],
            pincer_r=data['pincer_r'],
            unknown_0x63dcbbb6=data['unknown_0x63dcbbb6'],
            unknown_0x2393c3c0=data['unknown_0x2393c3c0'],
            spit_attack_visor_effect=data['spit_attack_visor_effect'],
            unknown_0x61f75902=data['unknown_0x61f75902'],
            charge_range_min=data['charge_range_min'],
            charge_range_max=data['charge_range_max'],
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            charge_impulse_horizontal=data['charge_impulse_horizontal'],
            charge_impulse_vertical=data['charge_impulse_vertical'],
            unknown_0x2b053901=data['unknown_0x2b053901'],
            unknown_0x47e969d3=data['unknown_0x47e969d3'],
            melee_impulse_horizontal=data['melee_impulse_horizontal'],
            melee_impulse_vertical=data['melee_impulse_vertical'],
            morphball_toss_damage=DamageInfo.from_json(data['morphball_toss_damage']),
            pincer_swipe_damage=DamageInfo.from_json(data['pincer_swipe_damage']),
            unknown_0xe593f1c6=data['unknown_0xe593f1c6'],
            unknown_0x3c5d53a4=data['unknown_0x3c5d53a4'],
            unknown_0xda3dfc45=data['unknown_0xda3dfc45'],
            pursuit_frustration_timer=data['pursuit_frustration_timer'],
            pursuit_frustration_radius=data['pursuit_frustration_radius'],
            can_link_transfer=data['can_link_transfer'],
            eye_glow=data['eye_glow'],
            part_0x3221407e=data['part_0x3221407e'],
            part_0x8b2a15ee=data['part_0x8b2a15ee'],
            part_0x526c6956=data['part_0x526c6956'],
            part_0xd24a1751=data['part_0xd24a1751'],
            ing_boss_bomb_damage=DamageInfo.from_json(data['ing_boss_bomb_damage']),
            unknown_0x3d58f51f=data['unknown_0x3d58f51f'],
            bomb_bounce_sound=data['bomb_bounce_sound'],
            bomb_explode_sound=data['bomb_explode_sound'],
            unknown_0x547f9400=data['unknown_0x547f9400'],
            unknown_0xefef7b45=data['unknown_0xefef7b45'],
            sandworm_struct_0xb8c15f15=SandwormStruct.from_json(data['sandworm_struct_0xb8c15f15']),
            sandworm_struct_0xce246628=SandwormStruct.from_json(data['sandworm_struct_0xce246628']),
            sandworm_struct_0x55578cfc=SandwormStruct.from_json(data['sandworm_struct_0x55578cfc']),
            sandworm_struct_0x23ee1452=SandwormStruct.from_json(data['sandworm_struct_0x23ee1452']),
            sandworm_struct_0xb89dfe86=SandwormStruct.from_json(data['sandworm_struct_0xb89dfe86']),
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0x06dee4c5': self.unknown_0x06dee4c5,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'pincer_scale': self.pincer_scale,
            'walk_sound': self.walk_sound,
            'walk_vocal_sound': self.walk_vocal_sound,
            'melee_attack_sound': self.melee_attack_sound,
            'eye_killed_sound': self.eye_killed_sound,
            'pincer_l': self.pincer_l,
            'pincer_r': self.pincer_r,
            'unknown_0x63dcbbb6': self.unknown_0x63dcbbb6,
            'unknown_0x2393c3c0': self.unknown_0x2393c3c0,
            'spit_attack_visor_effect': self.spit_attack_visor_effect,
            'unknown_0x61f75902': self.unknown_0x61f75902,
            'charge_range_min': self.charge_range_min,
            'charge_range_max': self.charge_range_max,
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'charge_impulse_horizontal': self.charge_impulse_horizontal,
            'charge_impulse_vertical': self.charge_impulse_vertical,
            'unknown_0x2b053901': self.unknown_0x2b053901,
            'unknown_0x47e969d3': self.unknown_0x47e969d3,
            'melee_impulse_horizontal': self.melee_impulse_horizontal,
            'melee_impulse_vertical': self.melee_impulse_vertical,
            'morphball_toss_damage': self.morphball_toss_damage.to_json(),
            'pincer_swipe_damage': self.pincer_swipe_damage.to_json(),
            'unknown_0xe593f1c6': self.unknown_0xe593f1c6,
            'unknown_0x3c5d53a4': self.unknown_0x3c5d53a4,
            'unknown_0xda3dfc45': self.unknown_0xda3dfc45,
            'pursuit_frustration_timer': self.pursuit_frustration_timer,
            'pursuit_frustration_radius': self.pursuit_frustration_radius,
            'can_link_transfer': self.can_link_transfer,
            'eye_glow': self.eye_glow,
            'part_0x3221407e': self.part_0x3221407e,
            'part_0x8b2a15ee': self.part_0x8b2a15ee,
            'part_0x526c6956': self.part_0x526c6956,
            'part_0xd24a1751': self.part_0xd24a1751,
            'ing_boss_bomb_damage': self.ing_boss_bomb_damage.to_json(),
            'unknown_0x3d58f51f': self.unknown_0x3d58f51f,
            'bomb_bounce_sound': self.bomb_bounce_sound,
            'bomb_explode_sound': self.bomb_explode_sound,
            'unknown_0x547f9400': self.unknown_0x547f9400,
            'unknown_0xefef7b45': self.unknown_0xefef7b45,
            'sandworm_struct_0xb8c15f15': self.sandworm_struct_0xb8c15f15.to_json(),
            'sandworm_struct_0xce246628': self.sandworm_struct_0xce246628.to_json(),
            'sandworm_struct_0x55578cfc': self.sandworm_struct_0x55578cfc.to_json(),
            'sandworm_struct_0x23ee1452': self.sandworm_struct_0x23ee1452.to_json(),
            'sandworm_struct_0xb89dfe86': self.sandworm_struct_0xb89dfe86.to_json(),
            'ing_possession_data': self.ing_possession_data.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0x06dee4c5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'detection_range': 32.0, 'collision_radius': 0.5, 'collision_height': 1.0, 'creature_size': 2})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_pincer_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_walk_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_walk_vocal_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_melee_attack_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_eye_killed_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_pincer_l(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_pincer_r(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x63dcbbb6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2393c3c0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_attack_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x61f75902(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_range_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_range_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_charge_impulse_horizontal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_impulse_vertical(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2b053901(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47e969d3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_impulse_horizontal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_impulse_vertical(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_toss_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_pincer_swipe_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0xe593f1c6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3c5d53a4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xda3dfc45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pursuit_frustration_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pursuit_frustration_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_link_transfer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_eye_glow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x3221407e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x8b2a15ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x526c6956(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xd24a1751(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_boss_bomb_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0x3d58f51f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_bomb_explode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x547f9400(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xefef7b45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sandworm_struct_0xb8c15f15(data: typing.BinaryIO, property_size: int):
    return SandwormStruct.from_stream(data, property_size)


def _decode_sandworm_struct_0xce246628(data: typing.BinaryIO, property_size: int):
    return SandwormStruct.from_stream(data, property_size)


def _decode_sandworm_struct_0x55578cfc(data: typing.BinaryIO, property_size: int):
    return SandwormStruct.from_stream(data, property_size)


def _decode_sandworm_struct_0x23ee1452(data: typing.BinaryIO, property_size: int):
    return SandwormStruct.from_stream(data, property_size)


def _decode_sandworm_struct_0xb89dfe86(data: typing.BinaryIO, property_size: int):
    return SandwormStruct.from_stream(data, property_size)


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6dee4c5: ('unknown_0x06dee4c5', _decode_unknown_0x06dee4c5),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x3db583ae: ('pincer_scale', _decode_pincer_scale),
    0xa24376ec: ('walk_sound', _decode_walk_sound),
    0xd35eb69d: ('walk_vocal_sound', _decode_walk_vocal_sound),
    0xaadaabb8: ('melee_attack_sound', _decode_melee_attack_sound),
    0x8128ce4a: ('eye_killed_sound', _decode_eye_killed_sound),
    0x66e34a08: ('pincer_l', _decode_pincer_l),
    0x5f3f29e3: ('pincer_r', _decode_pincer_r),
    0x63dcbbb6: ('unknown_0x63dcbbb6', _decode_unknown_0x63dcbbb6),
    0x2393c3c0: ('unknown_0x2393c3c0', _decode_unknown_0x2393c3c0),
    0xf9469e49: ('spit_attack_visor_effect', _decode_spit_attack_visor_effect),
    0x61f75902: ('unknown_0x61f75902', _decode_unknown_0x61f75902),
    0x2a7446ee: ('charge_range_min', _decode_charge_range_min),
    0xcc14e90f: ('charge_range_max', _decode_charge_range_max),
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x12090da8: ('charge_impulse_horizontal', _decode_charge_impulse_horizontal),
    0xc07bbe9a: ('charge_impulse_vertical', _decode_charge_impulse_vertical),
    0x2b053901: ('unknown_0x2b053901', _decode_unknown_0x2b053901),
    0x47e969d3: ('unknown_0x47e969d3', _decode_unknown_0x47e969d3),
    0xb8eecc95: ('melee_impulse_horizontal', _decode_melee_impulse_horizontal),
    0xf59af01a: ('melee_impulse_vertical', _decode_melee_impulse_vertical),
    0xf8fd6885: ('morphball_toss_damage', _decode_morphball_toss_damage),
    0x449233bc: ('pincer_swipe_damage', _decode_pincer_swipe_damage),
    0xe593f1c6: ('unknown_0xe593f1c6', _decode_unknown_0xe593f1c6),
    0x3c5d53a4: ('unknown_0x3c5d53a4', _decode_unknown_0x3c5d53a4),
    0xda3dfc45: ('unknown_0xda3dfc45', _decode_unknown_0xda3dfc45),
    0xdfa46e80: ('pursuit_frustration_timer', _decode_pursuit_frustration_timer),
    0x49f36a3f: ('pursuit_frustration_radius', _decode_pursuit_frustration_radius),
    0xb47dd18f: ('can_link_transfer', _decode_can_link_transfer),
    0xca82d3c: ('eye_glow', _decode_eye_glow),
    0x3221407e: ('part_0x3221407e', _decode_part_0x3221407e),
    0x8b2a15ee: ('part_0x8b2a15ee', _decode_part_0x8b2a15ee),
    0x526c6956: ('part_0x526c6956', _decode_part_0x526c6956),
    0xd24a1751: ('part_0xd24a1751', _decode_part_0xd24a1751),
    0x4461a8ad: ('ing_boss_bomb_damage', _decode_ing_boss_bomb_damage),
    0x3d58f51f: ('unknown_0x3d58f51f', _decode_unknown_0x3d58f51f),
    0x8c41066c: ('bomb_bounce_sound', _decode_bomb_bounce_sound),
    0x8649fe53: ('bomb_explode_sound', _decode_bomb_explode_sound),
    0x547f9400: ('unknown_0x547f9400', _decode_unknown_0x547f9400),
    0xefef7b45: ('unknown_0xefef7b45', _decode_unknown_0xefef7b45),
    0xb8c15f15: ('sandworm_struct_0xb8c15f15', _decode_sandworm_struct_0xb8c15f15),
    0xce246628: ('sandworm_struct_0xce246628', _decode_sandworm_struct_0xce246628),
    0x55578cfc: ('sandworm_struct_0x55578cfc', _decode_sandworm_struct_0x55578cfc),
    0x23ee1452: ('sandworm_struct_0x23ee1452', _decode_sandworm_struct_0x23ee1452),
    0xb89dfe86: ('sandworm_struct_0xb89dfe86', _decode_sandworm_struct_0xb89dfe86),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
}
