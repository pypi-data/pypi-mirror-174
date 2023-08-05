# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SpawnPointStruct(BaseProperty):
    power_beam: int = dataclasses.field(default=1)
    dark_beam: int = dataclasses.field(default=0)
    light_beam: int = dataclasses.field(default=0)
    annihilator_beam: int = dataclasses.field(default=0)
    power_beam_combo: int = dataclasses.field(default=1)
    dark_beam_combo: int = dataclasses.field(default=0)
    light_beam_combo: int = dataclasses.field(default=0)
    annihilator_beam_combo: int = dataclasses.field(default=0)
    charge_combo_upgrade: int = dataclasses.field(default=0)
    combat_visor: int = dataclasses.field(default=1)
    scan_visor: int = dataclasses.field(default=1)
    dark_visor: int = dataclasses.field(default=1)
    echo_visor: int = dataclasses.field(default=1)
    varia_suit: int = dataclasses.field(default=1)
    dark_suit: int = dataclasses.field(default=0)
    light_suit: int = dataclasses.field(default=0)
    morph_ball: int = dataclasses.field(default=1)
    boost_ball: int = dataclasses.field(default=1)
    spider_ball: int = dataclasses.field(default=1)
    bomb: int = dataclasses.field(default=1)
    light_bomb: int = dataclasses.field(default=1)
    dark_bomb: int = dataclasses.field(default=1)
    annihilator_bomb: int = dataclasses.field(default=1)
    charge_upgrade: int = dataclasses.field(default=1)  # Choice
    grapple_beam: int = dataclasses.field(default=0)
    double_jump: int = dataclasses.field(default=1)
    gravity_boost: int = dataclasses.field(default=1)
    seeker: int = dataclasses.field(default=1)
    screw_attack: int = dataclasses.field(default=0)
    translator_upgrade: int = dataclasses.field(default=0)
    temple_key1: int = dataclasses.field(default=0)
    temple_key2: int = dataclasses.field(default=0)
    temple_key3: int = dataclasses.field(default=0)
    temple_key4: int = dataclasses.field(default=0)
    temple_key5: int = dataclasses.field(default=0)
    temple_key6: int = dataclasses.field(default=0)
    temple_key7: int = dataclasses.field(default=0)
    temple_key8: int = dataclasses.field(default=0)
    temple_key9: int = dataclasses.field(default=0)
    sand_key1: int = dataclasses.field(default=0)
    sand_key2: int = dataclasses.field(default=0)
    sand_key3: int = dataclasses.field(default=0)
    swamp_key1: int = dataclasses.field(default=0)
    swamp_key2: int = dataclasses.field(default=0)
    swamp_key3: int = dataclasses.field(default=0)
    cliffside_key1: int = dataclasses.field(default=0)
    cliffside_key2: int = dataclasses.field(default=0)
    cliffside_key3: int = dataclasses.field(default=0)
    energy: int = dataclasses.field(default=0)
    energy_tank: int = dataclasses.field(default=0)
    unknown_0x161898dc: int = dataclasses.field(default=0)
    power_bomb: int = dataclasses.field(default=0)
    missile: int = dataclasses.field(default=5)
    dark_beam_ammo: int = dataclasses.field(default=5)
    light_beam_ammo: int = dataclasses.field(default=5)
    percentage_increase: int = dataclasses.field(default=0)
    misc_counter1: int = dataclasses.field(default=0)
    misc_counter2: int = dataclasses.field(default=0)
    misc_counter3: int = dataclasses.field(default=0)
    misc_counter4: int = dataclasses.field(default=0)
    change_to_power_beam: int = dataclasses.field(default=0)
    change_to_dark_beam: int = dataclasses.field(default=0)
    change_to_light_beam: int = dataclasses.field(default=0)
    change_to_annihilator_beam: int = dataclasses.field(default=0)
    multi_charge_upgrade: int = dataclasses.field(default=0)
    invisibility: int = dataclasses.field(default=0)
    amplified_damage: int = dataclasses.field(default=0)
    invincibility: int = dataclasses.field(default=0)
    unknown_0x66ae338e: int = dataclasses.field(default=0)
    unknown_0x210e495e: int = dataclasses.field(default=0)
    unknown_0x1c6e60ee: int = dataclasses.field(default=0)
    unknown_0xae4ebcfe: int = dataclasses.field(default=0)
    frag_count: int = dataclasses.field(default=0)
    died_count: int = dataclasses.field(default=0)
    archenemy_count: int = dataclasses.field(default=0)
    persistent_counter1: int = dataclasses.field(default=0)
    persistent_counter2: int = dataclasses.field(default=0)
    persistent_counter3: int = dataclasses.field(default=0)
    persistent_counter4: int = dataclasses.field(default=0)
    persistent_counter5: int = dataclasses.field(default=0)
    persistent_counter6: int = dataclasses.field(default=0)
    persistent_counter7: int = dataclasses.field(default=0)
    persistent_counter8: int = dataclasses.field(default=0)
    change_to_combat_visor: int = dataclasses.field(default=0)
    change_to_scan_visor: int = dataclasses.field(default=0)
    change_to_dark_visor: int = dataclasses.field(default=0)
    change_to_echo_visor: int = dataclasses.field(default=0)
    coin_amplifier: int = dataclasses.field(default=0)
    coin_counter: int = dataclasses.field(default=0)
    unlimited_missiles: int = dataclasses.field(default=0)
    unlimited_beam_ammo: int = dataclasses.field(default=0)
    dark_shield: int = dataclasses.field(default=0)
    light_shield: int = dataclasses.field(default=0)
    absorb_attack: int = dataclasses.field(default=0)
    death_ball: int = dataclasses.field(default=0)
    scan_virus: int = dataclasses.field(default=0)
    visor_static: int = dataclasses.field(default=0)
    beam_weapons_disabled: int = dataclasses.field(default=0)
    missile_weapons_disabled: int = dataclasses.field(default=0)
    unknown_0x32f5e918: int = dataclasses.field(default=0)
    disable_ball: int = dataclasses.field(default=0)
    disable_double_jump: int = dataclasses.field(default=0)
    activate_morphball_boost: int = dataclasses.field(default=0)
    hacked_effect: int = dataclasses.field(default=0)
    activate_morphball_damage: int = dataclasses.field(default=0)
    translator_upgrade1: int = dataclasses.field(default=0)
    translator_upgrade2: int = dataclasses.field(default=0)
    translator_upgrade3: int = dataclasses.field(default=0)
    translator_upgrade4: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00m')  # 109 properties

        data.write(b'\x9a\xcaE\xbc')  # 0x9aca45bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.power_beam))

        data.write(b'\x92\xbb\x94\xb7')  # 0x92bb94b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_beam))

        data.write(b'k\xe3@\xba')  # 0x6be340ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_beam))

        data.write(b'\xc7;,\x90')  # 0xc73b2c90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.annihilator_beam))

        data.write(b'\xef\xd4\xda\xbe')  # 0xefd4dabe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.power_beam_combo))

        data.write(b'\x9b\x06\xbd<')  # 0x9b06bd3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_beam_combo))

        data.write(b'mqr\xbf')  # 0x6d7172bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_beam_combo))

        data.write(b'\x16\xd8\x9a\xcc')  # 0x16d89acc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.annihilator_beam_combo))

        data.write(b'\xea\x86\xa2\xb9')  # 0xea86a2b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.charge_combo_upgrade))

        data.write(b'&\xa5\xe3\xc1')  # 0x26a5e3c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.combat_visor))

        data.write(b'\x9d\xe8s\x1d')  # 0x9de8731d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.scan_visor))

        data.write(b';\n\xb1\x0b')  # 0x3b0ab10b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_visor))

        data.write(b'\x95\xa3\x04\x88')  # 0x95a30488
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.echo_visor))

        data.write(b'\n\xb6\x03\xf7')  # 0xab603f7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.varia_suit))

        data.write(b'M\xa5R\x82')  # 0x4da55282
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_suit))

        data.write(b'\xb4\xfd\x86\x8f')  # 0xb4fd868f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_suit))

        data.write(b'>\xc5\xa9\xf5')  # 0x3ec5a9f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.morph_ball))

        data.write(b'\x8c\x98$}')  # 0x8c98247d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.boost_ball))

        data.write(b'\xbd\x8bT|')  # 0xbd8b547c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.spider_ball))

        data.write(b'S8v\x89')  # 0x53387689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.bomb))

        data.write(b'W\xeb\x9e\x8b')  # 0x57eb9e8b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_bomb))

        data.write(b'\xae\xb3J\x86')  # 0xaeb34a86
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_bomb))

        data.write(b'\xfb3\xf2\xa1')  # 0xfb33f2a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.annihilator_bomb))

        data.write(b'K\x15\xeb\x9a')  # 0x4b15eb9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.charge_upgrade))

        data.write(b'D\xfb\xb1\x9c')  # 0x44fbb19c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grapple_beam))

        data.write(b'\xf5[\xe1,')  # 0xf55be12c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.double_jump))

        data.write(b'\xbc%\xca\xed')  # 0xbc25caed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.gravity_boost))

        data.write(b'\nk7o')  # 0xa6b376f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.seeker))

        data.write(b'\xd8\xa9\xbb\xcb')  # 0xd8a9bbcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.screw_attack))

        data.write(b'}\x1c\x96\x85')  # 0x7d1c9685
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.translator_upgrade))

        data.write(b'\x8fl\xdc\xf9')  # 0x8f6cdcf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key1))

        data.write(b'\x9d\xd9s\x17')  # 0x9dd97317
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key2))

        data.write(b'%e\x14r')  # 0x25651472
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key3))

        data.write(b'\xb8\xb2,\xcb')  # 0xb8b22ccb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key4))

        data.write(b'\x00\x0eK\xae')  # 0xe4bae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key5))

        data.write(b'\x12\xbb\xe4@')  # 0x12bbe440
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key6))

        data.write(b'\xaa\x07\x83%')  # 0xaa078325
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key7))

        data.write(b'\xf2d\x93s')  # 0xf2649373
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key8))

        data.write(b'J\xd8\xf4\x16')  # 0x4ad8f416
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.temple_key9))

        data.write(b'\xc2q\xcf\xbc')  # 0xc271cfbc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sand_key1))

        data.write(b'\xd0\xc4`R')  # 0xd0c46052
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sand_key2))

        data.write(b'hx\x077')  # 0x68780737
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sand_key3))

        data.write(b'n\xff\xcf\x82')  # 0x6effcf82
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.swamp_key1))

        data.write(b'|J`l')  # 0x7c4a606c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.swamp_key2))

        data.write(b'\xc4\xf6\x07\t')  # 0xc4f60709
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.swamp_key3))

        data.write(b'\xc2\rb+')  # 0xc20d622b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cliffside_key1))

        data.write(b'\xd0\xb8\xcd\xc5')  # 0xd0b8cdc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cliffside_key2))

        data.write(b'h\x04\xaa\xa0')  # 0x6804aaa0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cliffside_key3))

        data.write(b'\x01\xc3\x97\xf0')  # 0x1c397f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.energy))

        data.write(b'\xfco\x86\x0c')  # 0xfc6f860c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.energy_tank))

        data.write(b'\x16\x18\x98\xdc')  # 0x161898dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x161898dc))

        data.write(b'\xa6\xc2\x9b\x8d')  # 0xa6c29b8d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.power_bomb))

        data.write(b'\xec\x7f\xb0\xef')  # 0xec7fb0ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.missile))

        data.write(b'\xfc\xec\xf7D')  # 0xfcecf744
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_beam_ammo))

        data.write(b'2\x05/\x91')  # 0x32052f91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_beam_ammo))

        data.write(b'n@8\xab')  # 0x6e4038ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.percentage_increase))

        data.write(b'\x148z\xab')  # 0x14387aab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.misc_counter1))

        data.write(b'\x06\x8d\xd5E')  # 0x68dd545
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.misc_counter2))

        data.write(b'\xbe1\xb2 ')  # 0xbe31b220
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.misc_counter3))

        data.write(b'#\xe6\x8a\x99')  # 0x23e68a99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.misc_counter4))

        data.write(b'\x8e\xcbfe')  # 0x8ecb6665
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_power_beam))

        data.write(b'\x92\xc4\x02\xab')  # 0x92c402ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_dark_beam))

        data.write(b'\x7f\xe2cc')  # 0x7fe26363
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_light_beam))

        data.write(b'\xd7\xf8Xj')  # 0xd7f8586a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_annihilator_beam))

        data.write(b"'\xd2T\xaf")  # 0x27d254af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.multi_charge_upgrade))

        data.write(b'\x19\x92d ')  # 0x19926420
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.invisibility))

        data.write(b'\xce(L\t')  # 0xce284c09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.amplified_damage))

        data.write(b'\xde\xc9\x99\xc3')  # 0xdec999c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.invincibility))

        data.write(b'f\xae3\x8e')  # 0x66ae338e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x66ae338e))

        data.write(b'!\x0eI^')  # 0x210e495e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x210e495e))

        data.write(b'\x1cn`\xee')  # 0x1c6e60ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1c6e60ee))

        data.write(b'\xaeN\xbc\xfe')  # 0xae4ebcfe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xae4ebcfe))

        data.write(b'SQ\xdb\xa5')  # 0x5351dba5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_count))

        data.write(b'\x02\xdb\x9a\n')  # 0x2db9a0a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.died_count))

        data.write(b'{\x98\x06Q')  # 0x7b980651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.archenemy_count))

        data.write(b'\xe9\x86\x1cI')  # 0xe9861c49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter1))

        data.write(b'\xfb3\xb3\xa7')  # 0xfb33b3a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter2))

        data.write(b'C\x8f\xd4\xc2')  # 0x438fd4c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter3))

        data.write(b'\xdeX\xec{')  # 0xde58ec7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter4))

        data.write(b'f\xe4\x8b\x1e')  # 0x66e48b1e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter5))

        data.write(b'tQ$\xf0')  # 0x745124f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter6))

        data.write(b'\xcc\xedC\x95')  # 0xcced4395
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter7))

        data.write(b'\x94\x8eS\xc3')  # 0x948e53c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.persistent_counter8))

        data.write(b'\xd48\xf8\xe4')  # 0xd438f8e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_combat_visor))

        data.write(b'\x89\xe9P\xc4')  # 0x89e950c4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_scan_visor))

        data.write(b'/\x0b\x92\xd2')  # 0x2f0b92d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_dark_visor))

        data.write(b"\x81\xa2'Q")  # 0x81a22751
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.change_to_echo_visor))

        data.write(b'\xdb\x8f\x0e\x87')  # 0xdb8f0e87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_amplifier))

        data.write(b'\xafo6\x1a')  # 0xaf6f361a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.coin_counter))

        data.write(b'\xae\x8d\xee\x81')  # 0xae8dee81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unlimited_missiles))

        data.write(b'\xd1\xff\xb4\x9f')  # 0xd1ffb49f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unlimited_beam_ammo))

        data.write(b'\xbcQ\xdeK')  # 0xbc51de4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_shield))

        data.write(b'\x88AO\x93')  # 0x88414f93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_shield))

        data.write(b'\xfb\xe2\x15\x90')  # 0xfbe21590
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.absorb_attack))

        data.write(b'\xd0\xb6\xa0\x07')  # 0xd0b6a007
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_ball))

        data.write(b'\xc4XH\xfe')  # 0xc45848fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.scan_virus))

        data.write(b'\x92\xb9\x16\xd7')  # 0x92b916d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.visor_static))

        data.write(b'\xa6%|\xd8')  # 0xa6257cd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.beam_weapons_disabled))

        data.write(b'k\xf2L$')  # 0x6bf24c24
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.missile_weapons_disabled))

        data.write(b'2\xf5\xe9\x18')  # 0x32f5e918
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x32f5e918))

        data.write(b'\x1c\xe9UA')  # 0x1ce95541
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.disable_ball))

        data.write(b']\xd9\x00M')  # 0x5dd9004d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.disable_double_jump))

        data.write(b'\xf6O\x1d\xbd')  # 0xf64f1dbd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.activate_morphball_boost))

        data.write(b'v\x00\r\x1e')  # 0x76000d1e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.hacked_effect))

        data.write(b'\x85\xabR\xbc')  # 0x85ab52bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.activate_morphball_damage))

        data.write(b'q\x1c\x15\x0f')  # 0x711c150f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.translator_upgrade1))

        data.write(b'c\xa9\xba\xe1')  # 0x63a9bae1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.translator_upgrade2))

        data.write(b'\xdb\x15\xdd\x84')  # 0xdb15dd84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.translator_upgrade3))

        data.write(b'F\xc2\xe5=')  # 0x46c2e53d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.translator_upgrade4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power_beam=data['power_beam'],
            dark_beam=data['dark_beam'],
            light_beam=data['light_beam'],
            annihilator_beam=data['annihilator_beam'],
            power_beam_combo=data['power_beam_combo'],
            dark_beam_combo=data['dark_beam_combo'],
            light_beam_combo=data['light_beam_combo'],
            annihilator_beam_combo=data['annihilator_beam_combo'],
            charge_combo_upgrade=data['charge_combo_upgrade'],
            combat_visor=data['combat_visor'],
            scan_visor=data['scan_visor'],
            dark_visor=data['dark_visor'],
            echo_visor=data['echo_visor'],
            varia_suit=data['varia_suit'],
            dark_suit=data['dark_suit'],
            light_suit=data['light_suit'],
            morph_ball=data['morph_ball'],
            boost_ball=data['boost_ball'],
            spider_ball=data['spider_ball'],
            bomb=data['bomb'],
            light_bomb=data['light_bomb'],
            dark_bomb=data['dark_bomb'],
            annihilator_bomb=data['annihilator_bomb'],
            charge_upgrade=data['charge_upgrade'],
            grapple_beam=data['grapple_beam'],
            double_jump=data['double_jump'],
            gravity_boost=data['gravity_boost'],
            seeker=data['seeker'],
            screw_attack=data['screw_attack'],
            translator_upgrade=data['translator_upgrade'],
            temple_key1=data['temple_key1'],
            temple_key2=data['temple_key2'],
            temple_key3=data['temple_key3'],
            temple_key4=data['temple_key4'],
            temple_key5=data['temple_key5'],
            temple_key6=data['temple_key6'],
            temple_key7=data['temple_key7'],
            temple_key8=data['temple_key8'],
            temple_key9=data['temple_key9'],
            sand_key1=data['sand_key1'],
            sand_key2=data['sand_key2'],
            sand_key3=data['sand_key3'],
            swamp_key1=data['swamp_key1'],
            swamp_key2=data['swamp_key2'],
            swamp_key3=data['swamp_key3'],
            cliffside_key1=data['cliffside_key1'],
            cliffside_key2=data['cliffside_key2'],
            cliffside_key3=data['cliffside_key3'],
            energy=data['energy'],
            energy_tank=data['energy_tank'],
            unknown_0x161898dc=data['unknown_0x161898dc'],
            power_bomb=data['power_bomb'],
            missile=data['missile'],
            dark_beam_ammo=data['dark_beam_ammo'],
            light_beam_ammo=data['light_beam_ammo'],
            percentage_increase=data['percentage_increase'],
            misc_counter1=data['misc_counter1'],
            misc_counter2=data['misc_counter2'],
            misc_counter3=data['misc_counter3'],
            misc_counter4=data['misc_counter4'],
            change_to_power_beam=data['change_to_power_beam'],
            change_to_dark_beam=data['change_to_dark_beam'],
            change_to_light_beam=data['change_to_light_beam'],
            change_to_annihilator_beam=data['change_to_annihilator_beam'],
            multi_charge_upgrade=data['multi_charge_upgrade'],
            invisibility=data['invisibility'],
            amplified_damage=data['amplified_damage'],
            invincibility=data['invincibility'],
            unknown_0x66ae338e=data['unknown_0x66ae338e'],
            unknown_0x210e495e=data['unknown_0x210e495e'],
            unknown_0x1c6e60ee=data['unknown_0x1c6e60ee'],
            unknown_0xae4ebcfe=data['unknown_0xae4ebcfe'],
            frag_count=data['frag_count'],
            died_count=data['died_count'],
            archenemy_count=data['archenemy_count'],
            persistent_counter1=data['persistent_counter1'],
            persistent_counter2=data['persistent_counter2'],
            persistent_counter3=data['persistent_counter3'],
            persistent_counter4=data['persistent_counter4'],
            persistent_counter5=data['persistent_counter5'],
            persistent_counter6=data['persistent_counter6'],
            persistent_counter7=data['persistent_counter7'],
            persistent_counter8=data['persistent_counter8'],
            change_to_combat_visor=data['change_to_combat_visor'],
            change_to_scan_visor=data['change_to_scan_visor'],
            change_to_dark_visor=data['change_to_dark_visor'],
            change_to_echo_visor=data['change_to_echo_visor'],
            coin_amplifier=data['coin_amplifier'],
            coin_counter=data['coin_counter'],
            unlimited_missiles=data['unlimited_missiles'],
            unlimited_beam_ammo=data['unlimited_beam_ammo'],
            dark_shield=data['dark_shield'],
            light_shield=data['light_shield'],
            absorb_attack=data['absorb_attack'],
            death_ball=data['death_ball'],
            scan_virus=data['scan_virus'],
            visor_static=data['visor_static'],
            beam_weapons_disabled=data['beam_weapons_disabled'],
            missile_weapons_disabled=data['missile_weapons_disabled'],
            unknown_0x32f5e918=data['unknown_0x32f5e918'],
            disable_ball=data['disable_ball'],
            disable_double_jump=data['disable_double_jump'],
            activate_morphball_boost=data['activate_morphball_boost'],
            hacked_effect=data['hacked_effect'],
            activate_morphball_damage=data['activate_morphball_damage'],
            translator_upgrade1=data['translator_upgrade1'],
            translator_upgrade2=data['translator_upgrade2'],
            translator_upgrade3=data['translator_upgrade3'],
            translator_upgrade4=data['translator_upgrade4'],
        )

    def to_json(self) -> dict:
        return {
            'power_beam': self.power_beam,
            'dark_beam': self.dark_beam,
            'light_beam': self.light_beam,
            'annihilator_beam': self.annihilator_beam,
            'power_beam_combo': self.power_beam_combo,
            'dark_beam_combo': self.dark_beam_combo,
            'light_beam_combo': self.light_beam_combo,
            'annihilator_beam_combo': self.annihilator_beam_combo,
            'charge_combo_upgrade': self.charge_combo_upgrade,
            'combat_visor': self.combat_visor,
            'scan_visor': self.scan_visor,
            'dark_visor': self.dark_visor,
            'echo_visor': self.echo_visor,
            'varia_suit': self.varia_suit,
            'dark_suit': self.dark_suit,
            'light_suit': self.light_suit,
            'morph_ball': self.morph_ball,
            'boost_ball': self.boost_ball,
            'spider_ball': self.spider_ball,
            'bomb': self.bomb,
            'light_bomb': self.light_bomb,
            'dark_bomb': self.dark_bomb,
            'annihilator_bomb': self.annihilator_bomb,
            'charge_upgrade': self.charge_upgrade,
            'grapple_beam': self.grapple_beam,
            'double_jump': self.double_jump,
            'gravity_boost': self.gravity_boost,
            'seeker': self.seeker,
            'screw_attack': self.screw_attack,
            'translator_upgrade': self.translator_upgrade,
            'temple_key1': self.temple_key1,
            'temple_key2': self.temple_key2,
            'temple_key3': self.temple_key3,
            'temple_key4': self.temple_key4,
            'temple_key5': self.temple_key5,
            'temple_key6': self.temple_key6,
            'temple_key7': self.temple_key7,
            'temple_key8': self.temple_key8,
            'temple_key9': self.temple_key9,
            'sand_key1': self.sand_key1,
            'sand_key2': self.sand_key2,
            'sand_key3': self.sand_key3,
            'swamp_key1': self.swamp_key1,
            'swamp_key2': self.swamp_key2,
            'swamp_key3': self.swamp_key3,
            'cliffside_key1': self.cliffside_key1,
            'cliffside_key2': self.cliffside_key2,
            'cliffside_key3': self.cliffside_key3,
            'energy': self.energy,
            'energy_tank': self.energy_tank,
            'unknown_0x161898dc': self.unknown_0x161898dc,
            'power_bomb': self.power_bomb,
            'missile': self.missile,
            'dark_beam_ammo': self.dark_beam_ammo,
            'light_beam_ammo': self.light_beam_ammo,
            'percentage_increase': self.percentage_increase,
            'misc_counter1': self.misc_counter1,
            'misc_counter2': self.misc_counter2,
            'misc_counter3': self.misc_counter3,
            'misc_counter4': self.misc_counter4,
            'change_to_power_beam': self.change_to_power_beam,
            'change_to_dark_beam': self.change_to_dark_beam,
            'change_to_light_beam': self.change_to_light_beam,
            'change_to_annihilator_beam': self.change_to_annihilator_beam,
            'multi_charge_upgrade': self.multi_charge_upgrade,
            'invisibility': self.invisibility,
            'amplified_damage': self.amplified_damage,
            'invincibility': self.invincibility,
            'unknown_0x66ae338e': self.unknown_0x66ae338e,
            'unknown_0x210e495e': self.unknown_0x210e495e,
            'unknown_0x1c6e60ee': self.unknown_0x1c6e60ee,
            'unknown_0xae4ebcfe': self.unknown_0xae4ebcfe,
            'frag_count': self.frag_count,
            'died_count': self.died_count,
            'archenemy_count': self.archenemy_count,
            'persistent_counter1': self.persistent_counter1,
            'persistent_counter2': self.persistent_counter2,
            'persistent_counter3': self.persistent_counter3,
            'persistent_counter4': self.persistent_counter4,
            'persistent_counter5': self.persistent_counter5,
            'persistent_counter6': self.persistent_counter6,
            'persistent_counter7': self.persistent_counter7,
            'persistent_counter8': self.persistent_counter8,
            'change_to_combat_visor': self.change_to_combat_visor,
            'change_to_scan_visor': self.change_to_scan_visor,
            'change_to_dark_visor': self.change_to_dark_visor,
            'change_to_echo_visor': self.change_to_echo_visor,
            'coin_amplifier': self.coin_amplifier,
            'coin_counter': self.coin_counter,
            'unlimited_missiles': self.unlimited_missiles,
            'unlimited_beam_ammo': self.unlimited_beam_ammo,
            'dark_shield': self.dark_shield,
            'light_shield': self.light_shield,
            'absorb_attack': self.absorb_attack,
            'death_ball': self.death_ball,
            'scan_virus': self.scan_virus,
            'visor_static': self.visor_static,
            'beam_weapons_disabled': self.beam_weapons_disabled,
            'missile_weapons_disabled': self.missile_weapons_disabled,
            'unknown_0x32f5e918': self.unknown_0x32f5e918,
            'disable_ball': self.disable_ball,
            'disable_double_jump': self.disable_double_jump,
            'activate_morphball_boost': self.activate_morphball_boost,
            'hacked_effect': self.hacked_effect,
            'activate_morphball_damage': self.activate_morphball_damage,
            'translator_upgrade1': self.translator_upgrade1,
            'translator_upgrade2': self.translator_upgrade2,
            'translator_upgrade3': self.translator_upgrade3,
            'translator_upgrade4': self.translator_upgrade4,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x9aca45bc, 0x92bb94b7, 0x6be340ba, 0xc73b2c90, 0xefd4dabe, 0x9b06bd3c, 0x6d7172bf, 0x16d89acc, 0xea86a2b9, 0x26a5e3c1, 0x9de8731d, 0x3b0ab10b, 0x95a30488, 0xab603f7, 0x4da55282, 0xb4fd868f, 0x3ec5a9f5, 0x8c98247d, 0xbd8b547c, 0x53387689, 0x57eb9e8b, 0xaeb34a86, 0xfb33f2a1, 0x4b15eb9a, 0x44fbb19c, 0xf55be12c, 0xbc25caed, 0xa6b376f, 0xd8a9bbcb, 0x7d1c9685, 0x8f6cdcf9, 0x9dd97317, 0x25651472, 0xb8b22ccb, 0xe4bae, 0x12bbe440, 0xaa078325, 0xf2649373, 0x4ad8f416, 0xc271cfbc, 0xd0c46052, 0x68780737, 0x6effcf82, 0x7c4a606c, 0xc4f60709, 0xc20d622b, 0xd0b8cdc5, 0x6804aaa0, 0x1c397f0, 0xfc6f860c, 0x161898dc, 0xa6c29b8d, 0xec7fb0ef, 0xfcecf744, 0x32052f91, 0x6e4038ab, 0x14387aab, 0x68dd545, 0xbe31b220, 0x23e68a99, 0x8ecb6665, 0x92c402ab, 0x7fe26363, 0xd7f8586a, 0x27d254af, 0x19926420, 0xce284c09, 0xdec999c3, 0x66ae338e, 0x210e495e, 0x1c6e60ee, 0xae4ebcfe, 0x5351dba5, 0x2db9a0a, 0x7b980651, 0xe9861c49, 0xfb33b3a7, 0x438fd4c2, 0xde58ec7b, 0x66e48b1e, 0x745124f0, 0xcced4395, 0x948e53c3, 0xd438f8e4, 0x89e950c4, 0x2f0b92d2, 0x81a22751, 0xdb8f0e87, 0xaf6f361a, 0xae8dee81, 0xd1ffb49f, 0xbc51de4b, 0x88414f93, 0xfbe21590, 0xd0b6a007, 0xc45848fe, 0x92b916d7, 0xa6257cd8, 0x6bf24c24, 0x32f5e918, 0x1ce95541, 0x5dd9004d, 0xf64f1dbd, 0x76000d1e, 0x85ab52bc, 0x711c150f, 0x63a9bae1, 0xdb15dd84, 0x46c2e53d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SpawnPointStruct]:
    if property_count != 109:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHLLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHlLHl')

    dec = _FAST_FORMAT.unpack(data.read(1090))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72], dec[75], dec[78], dec[81], dec[84], dec[87], dec[90], dec[93], dec[96], dec[99], dec[102], dec[105], dec[108], dec[111], dec[114], dec[117], dec[120], dec[123], dec[126], dec[129], dec[132], dec[135], dec[138], dec[141], dec[144], dec[147], dec[150], dec[153], dec[156], dec[159], dec[162], dec[165], dec[168], dec[171], dec[174], dec[177], dec[180], dec[183], dec[186], dec[189], dec[192], dec[195], dec[198], dec[201], dec[204], dec[207], dec[210], dec[213], dec[216], dec[219], dec[222], dec[225], dec[228], dec[231], dec[234], dec[237], dec[240], dec[243], dec[246], dec[249], dec[252], dec[255], dec[258], dec[261], dec[264], dec[267], dec[270], dec[273], dec[276], dec[279], dec[282], dec[285], dec[288], dec[291], dec[294], dec[297], dec[300], dec[303], dec[306], dec[309], dec[312], dec[315], dec[318], dec[321], dec[324]) != _FAST_IDS:
        return None

    return SpawnPointStruct(
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
        dec[89],
        dec[92],
        dec[95],
        dec[98],
        dec[101],
        dec[104],
        dec[107],
        dec[110],
        dec[113],
        dec[116],
        dec[119],
        dec[122],
        dec[125],
        dec[128],
        dec[131],
        dec[134],
        dec[137],
        dec[140],
        dec[143],
        dec[146],
        dec[149],
        dec[152],
        dec[155],
        dec[158],
        dec[161],
        dec[164],
        dec[167],
        dec[170],
        dec[173],
        dec[176],
        dec[179],
        dec[182],
        dec[185],
        dec[188],
        dec[191],
        dec[194],
        dec[197],
        dec[200],
        dec[203],
        dec[206],
        dec[209],
        dec[212],
        dec[215],
        dec[218],
        dec[221],
        dec[224],
        dec[227],
        dec[230],
        dec[233],
        dec[236],
        dec[239],
        dec[242],
        dec[245],
        dec[248],
        dec[251],
        dec[254],
        dec[257],
        dec[260],
        dec[263],
        dec[266],
        dec[269],
        dec[272],
        dec[275],
        dec[278],
        dec[281],
        dec[284],
        dec[287],
        dec[290],
        dec[293],
        dec[296],
        dec[299],
        dec[302],
        dec[305],
        dec[308],
        dec[311],
        dec[314],
        dec[317],
        dec[320],
        dec[323],
        dec[326],
    )


def _decode_power_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_annihilator_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_power_beam_combo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_beam_combo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_beam_combo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_annihilator_beam_combo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_charge_combo_upgrade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_combat_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_scan_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_echo_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_varia_suit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_suit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_suit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_morph_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_boost_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spider_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_annihilator_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_charge_upgrade(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grapple_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_double_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_gravity_boost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_seeker(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_screw_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_translator_upgrade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_temple_key9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sand_key1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sand_key2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sand_key3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_swamp_key1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_swamp_key2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_swamp_key3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cliffside_key1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cliffside_key2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cliffside_key3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_energy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_energy_tank(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x161898dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_power_bomb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_missile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_beam_ammo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_beam_ammo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_percentage_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_misc_counter1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_misc_counter2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_misc_counter3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_misc_counter4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_power_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_dark_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_light_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_annihilator_beam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_multi_charge_upgrade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_invisibility(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_amplified_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_invincibility(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x66ae338e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x210e495e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1c6e60ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xae4ebcfe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frag_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_died_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_archenemy_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_persistent_counter8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_combat_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_scan_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_dark_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_change_to_echo_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_amplifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_coin_counter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unlimited_missiles(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unlimited_beam_ammo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_absorb_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_scan_virus(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_visor_static(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_beam_weapons_disabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_missile_weapons_disabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x32f5e918(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_disable_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_disable_double_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_activate_morphball_boost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hacked_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_activate_morphball_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_translator_upgrade1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_translator_upgrade2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_translator_upgrade3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_translator_upgrade4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9aca45bc: ('power_beam', _decode_power_beam),
    0x92bb94b7: ('dark_beam', _decode_dark_beam),
    0x6be340ba: ('light_beam', _decode_light_beam),
    0xc73b2c90: ('annihilator_beam', _decode_annihilator_beam),
    0xefd4dabe: ('power_beam_combo', _decode_power_beam_combo),
    0x9b06bd3c: ('dark_beam_combo', _decode_dark_beam_combo),
    0x6d7172bf: ('light_beam_combo', _decode_light_beam_combo),
    0x16d89acc: ('annihilator_beam_combo', _decode_annihilator_beam_combo),
    0xea86a2b9: ('charge_combo_upgrade', _decode_charge_combo_upgrade),
    0x26a5e3c1: ('combat_visor', _decode_combat_visor),
    0x9de8731d: ('scan_visor', _decode_scan_visor),
    0x3b0ab10b: ('dark_visor', _decode_dark_visor),
    0x95a30488: ('echo_visor', _decode_echo_visor),
    0xab603f7: ('varia_suit', _decode_varia_suit),
    0x4da55282: ('dark_suit', _decode_dark_suit),
    0xb4fd868f: ('light_suit', _decode_light_suit),
    0x3ec5a9f5: ('morph_ball', _decode_morph_ball),
    0x8c98247d: ('boost_ball', _decode_boost_ball),
    0xbd8b547c: ('spider_ball', _decode_spider_ball),
    0x53387689: ('bomb', _decode_bomb),
    0x57eb9e8b: ('light_bomb', _decode_light_bomb),
    0xaeb34a86: ('dark_bomb', _decode_dark_bomb),
    0xfb33f2a1: ('annihilator_bomb', _decode_annihilator_bomb),
    0x4b15eb9a: ('charge_upgrade', _decode_charge_upgrade),
    0x44fbb19c: ('grapple_beam', _decode_grapple_beam),
    0xf55be12c: ('double_jump', _decode_double_jump),
    0xbc25caed: ('gravity_boost', _decode_gravity_boost),
    0xa6b376f: ('seeker', _decode_seeker),
    0xd8a9bbcb: ('screw_attack', _decode_screw_attack),
    0x7d1c9685: ('translator_upgrade', _decode_translator_upgrade),
    0x8f6cdcf9: ('temple_key1', _decode_temple_key1),
    0x9dd97317: ('temple_key2', _decode_temple_key2),
    0x25651472: ('temple_key3', _decode_temple_key3),
    0xb8b22ccb: ('temple_key4', _decode_temple_key4),
    0xe4bae: ('temple_key5', _decode_temple_key5),
    0x12bbe440: ('temple_key6', _decode_temple_key6),
    0xaa078325: ('temple_key7', _decode_temple_key7),
    0xf2649373: ('temple_key8', _decode_temple_key8),
    0x4ad8f416: ('temple_key9', _decode_temple_key9),
    0xc271cfbc: ('sand_key1', _decode_sand_key1),
    0xd0c46052: ('sand_key2', _decode_sand_key2),
    0x68780737: ('sand_key3', _decode_sand_key3),
    0x6effcf82: ('swamp_key1', _decode_swamp_key1),
    0x7c4a606c: ('swamp_key2', _decode_swamp_key2),
    0xc4f60709: ('swamp_key3', _decode_swamp_key3),
    0xc20d622b: ('cliffside_key1', _decode_cliffside_key1),
    0xd0b8cdc5: ('cliffside_key2', _decode_cliffside_key2),
    0x6804aaa0: ('cliffside_key3', _decode_cliffside_key3),
    0x1c397f0: ('energy', _decode_energy),
    0xfc6f860c: ('energy_tank', _decode_energy_tank),
    0x161898dc: ('unknown_0x161898dc', _decode_unknown_0x161898dc),
    0xa6c29b8d: ('power_bomb', _decode_power_bomb),
    0xec7fb0ef: ('missile', _decode_missile),
    0xfcecf744: ('dark_beam_ammo', _decode_dark_beam_ammo),
    0x32052f91: ('light_beam_ammo', _decode_light_beam_ammo),
    0x6e4038ab: ('percentage_increase', _decode_percentage_increase),
    0x14387aab: ('misc_counter1', _decode_misc_counter1),
    0x68dd545: ('misc_counter2', _decode_misc_counter2),
    0xbe31b220: ('misc_counter3', _decode_misc_counter3),
    0x23e68a99: ('misc_counter4', _decode_misc_counter4),
    0x8ecb6665: ('change_to_power_beam', _decode_change_to_power_beam),
    0x92c402ab: ('change_to_dark_beam', _decode_change_to_dark_beam),
    0x7fe26363: ('change_to_light_beam', _decode_change_to_light_beam),
    0xd7f8586a: ('change_to_annihilator_beam', _decode_change_to_annihilator_beam),
    0x27d254af: ('multi_charge_upgrade', _decode_multi_charge_upgrade),
    0x19926420: ('invisibility', _decode_invisibility),
    0xce284c09: ('amplified_damage', _decode_amplified_damage),
    0xdec999c3: ('invincibility', _decode_invincibility),
    0x66ae338e: ('unknown_0x66ae338e', _decode_unknown_0x66ae338e),
    0x210e495e: ('unknown_0x210e495e', _decode_unknown_0x210e495e),
    0x1c6e60ee: ('unknown_0x1c6e60ee', _decode_unknown_0x1c6e60ee),
    0xae4ebcfe: ('unknown_0xae4ebcfe', _decode_unknown_0xae4ebcfe),
    0x5351dba5: ('frag_count', _decode_frag_count),
    0x2db9a0a: ('died_count', _decode_died_count),
    0x7b980651: ('archenemy_count', _decode_archenemy_count),
    0xe9861c49: ('persistent_counter1', _decode_persistent_counter1),
    0xfb33b3a7: ('persistent_counter2', _decode_persistent_counter2),
    0x438fd4c2: ('persistent_counter3', _decode_persistent_counter3),
    0xde58ec7b: ('persistent_counter4', _decode_persistent_counter4),
    0x66e48b1e: ('persistent_counter5', _decode_persistent_counter5),
    0x745124f0: ('persistent_counter6', _decode_persistent_counter6),
    0xcced4395: ('persistent_counter7', _decode_persistent_counter7),
    0x948e53c3: ('persistent_counter8', _decode_persistent_counter8),
    0xd438f8e4: ('change_to_combat_visor', _decode_change_to_combat_visor),
    0x89e950c4: ('change_to_scan_visor', _decode_change_to_scan_visor),
    0x2f0b92d2: ('change_to_dark_visor', _decode_change_to_dark_visor),
    0x81a22751: ('change_to_echo_visor', _decode_change_to_echo_visor),
    0xdb8f0e87: ('coin_amplifier', _decode_coin_amplifier),
    0xaf6f361a: ('coin_counter', _decode_coin_counter),
    0xae8dee81: ('unlimited_missiles', _decode_unlimited_missiles),
    0xd1ffb49f: ('unlimited_beam_ammo', _decode_unlimited_beam_ammo),
    0xbc51de4b: ('dark_shield', _decode_dark_shield),
    0x88414f93: ('light_shield', _decode_light_shield),
    0xfbe21590: ('absorb_attack', _decode_absorb_attack),
    0xd0b6a007: ('death_ball', _decode_death_ball),
    0xc45848fe: ('scan_virus', _decode_scan_virus),
    0x92b916d7: ('visor_static', _decode_visor_static),
    0xa6257cd8: ('beam_weapons_disabled', _decode_beam_weapons_disabled),
    0x6bf24c24: ('missile_weapons_disabled', _decode_missile_weapons_disabled),
    0x32f5e918: ('unknown_0x32f5e918', _decode_unknown_0x32f5e918),
    0x1ce95541: ('disable_ball', _decode_disable_ball),
    0x5dd9004d: ('disable_double_jump', _decode_disable_double_jump),
    0xf64f1dbd: ('activate_morphball_boost', _decode_activate_morphball_boost),
    0x76000d1e: ('hacked_effect', _decode_hacked_effect),
    0x85ab52bc: ('activate_morphball_damage', _decode_activate_morphball_damage),
    0x711c150f: ('translator_upgrade1', _decode_translator_upgrade1),
    0x63a9bae1: ('translator_upgrade2', _decode_translator_upgrade2),
    0xdb15dd84: ('translator_upgrade3', _decode_translator_upgrade3),
    0x46c2e53d: ('translator_upgrade4', _decode_translator_upgrade4),
}
