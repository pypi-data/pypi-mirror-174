# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class Misc(BaseProperty):
    unknown_0x8ed04c36: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x94bb7ee5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_tweak_open_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x415a81f8: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xfe95100f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_fullscreen_bg_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x66733e29: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_frame_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_icons_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_text_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_highlight_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    pause_screen_helmet_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    gui_cursor_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdb5c8a60: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x166c22e0: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xcec78e81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x91338f72: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_memo_text_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_memo_text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc8ddc662: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_glow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5c336f85: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdefca700: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    selected_visor_beam_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unselected_visor_beam_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_filled_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_low_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_damage_modulate_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    damage_indicator_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_title_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    hud_title_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe7070332: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x779c7b9c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_warning_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_warning_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x83040135: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3c1ae0ff: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_bar_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_bar_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xbe3c29a1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_combo_charge_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4c5aff4f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0b17b693: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8b0a4c90: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_warning_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_warning_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x78522461: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    flash_pass_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x79ea6f12: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdc901206: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc54fa7bc: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x18717fa7: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8b7d7378: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x867b01a2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc02eed79: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    metroid_suck_pulse_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xce7c9d8d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_damage_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xafe2d45d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_holo_grid_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_ticks_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_seeker_ticks_outer_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_top_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_bottom_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_left_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_right_puzzle_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    x_ray_corner_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa947a67c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x421bae2a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x439a3774: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x8ee94c81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x716e6398: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    steam_no_blur_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0f37e756: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf7283644: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x37564b7d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x66b7eda3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf895098f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x9b27be10: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x6c8550c9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5368a35f: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x5a807b81: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xeb63afed: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_images_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xd3bafaf5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_damage_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4f1d443e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x0f6451da: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    scan_seeker_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x43ed3310: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa781ed1d: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    log_book_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    log_book_frame_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    inventory_equipped_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    command_text_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    command_text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x4b03e738: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xf883607c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb68f96ec: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x2e73549a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x938f3af5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x3f27fa9a: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xd2fa7631: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdfcf84e1: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x16912ca9: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe50cda52: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x7dc076a6: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xc6f86bfd: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xbfffe95a: int = dataclasses.field(default=5)

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
        data.write(b'\x00p')  # 112 properties

        data.write(b'\x8e\xd0L6')  # 0x8ed04c36
        data.write(b'\x00\x10')  # size
        self.unknown_0x8ed04c36.to_stream(data)

        data.write(b'\x94\xbb~\xe5')  # 0x94bb7ee5
        data.write(b'\x00\x10')  # size
        self.unknown_0x94bb7ee5.to_stream(data)

        data.write(b'-\x03{Z')  # 0x2d037b5a
        data.write(b'\x00\x10')  # size
        self.pause_screen_tweak_open_color.to_stream(data)

        data.write(b'AZ\x81\xf8')  # 0x415a81f8
        data.write(b'\x00\x10')  # size
        self.unknown_0x415a81f8.to_stream(data)

        data.write(b'\xfe\x95\x10\x0f')  # 0xfe95100f
        data.write(b'\x00\x10')  # size
        self.unknown_0xfe95100f.to_stream(data)

        data.write(b'\xaf8\xa7\x96')  # 0xaf38a796
        data.write(b'\x00\x10')  # size
        self.pause_screen_fullscreen_bg_color.to_stream(data)

        data.write(b'fs>)')  # 0x66733e29
        data.write(b'\x00\x10')  # size
        self.unknown_0x66733e29.to_stream(data)

        data.write(b'\xffm1\xe9')  # 0xff6d31e9
        data.write(b'\x00\x10')  # size
        self.pause_screen_frame_color.to_stream(data)

        data.write(b'\x9bc\xff\xa6')  # 0x9b63ffa6
        data.write(b'\x00\x10')  # size
        self.pause_screen_icons_color.to_stream(data)

        data.write(b'r\x98\xe2#')  # 0x7298e223
        data.write(b'\x00\x10')  # size
        self.pause_screen_text_color.to_stream(data)

        data.write(b'Ud\x81\xe8')  # 0x556481e8
        data.write(b'\x00\x10')  # size
        self.pause_screen_highlight_color.to_stream(data)

        data.write(b'\xee\x8a!\x17')  # 0xee8a2117
        data.write(b'\x00\x10')  # size
        self.pause_screen_helmet_color.to_stream(data)

        data.write(b'\xf4hi]')  # 0xf468695d
        data.write(b'\x00\x10')  # size
        self.gui_cursor_color.to_stream(data)

        data.write(b'\xdb\\\x8a`')  # 0xdb5c8a60
        data.write(b'\x00\x10')  # size
        self.unknown_0xdb5c8a60.to_stream(data)

        data.write(b'\x16l"\xe0')  # 0x166c22e0
        data.write(b'\x00\x10')  # size
        self.unknown_0x166c22e0.to_stream(data)

        data.write(b'\xce\xc7\x8e\x81')  # 0xcec78e81
        data.write(b'\x00\x10')  # size
        self.unknown_0xcec78e81.to_stream(data)

        data.write(b'\x913\x8fr')  # 0x91338f72
        data.write(b'\x00\x10')  # size
        self.unknown_0x91338f72.to_stream(data)

        data.write(b'-\xf1\xeb\x03')  # 0x2df1eb03
        data.write(b'\x00\x10')  # size
        self.hud_memo_text_foreground_color.to_stream(data)

        data.write(b'\xb5\xda0\xf4')  # 0xb5da30f4
        data.write(b'\x00\x10')  # size
        self.hud_memo_text_outline_color.to_stream(data)

        data.write(b'\xc8\xdd\xc6b')  # 0xc8ddc662
        data.write(b'\x00\x10')  # size
        self.unknown_0xc8ddc662.to_stream(data)

        data.write(b'i\x91\xe2\xcd')  # 0x6991e2cd
        data.write(b'\x00\x10')  # size
        self.hud_glow_color.to_stream(data)

        data.write(b'\\3o\x85')  # 0x5c336f85
        data.write(b'\x00\x10')  # size
        self.unknown_0x5c336f85.to_stream(data)

        data.write(b'\xde\xfc\xa7\x00')  # 0xdefca700
        data.write(b'\x00\x10')  # size
        self.unknown_0xdefca700.to_stream(data)

        data.write(b'\xcb}\xda\xf4')  # 0xcb7ddaf4
        data.write(b'\x00\x10')  # size
        self.selected_visor_beam_color.to_stream(data)

        data.write(b'\xf1y\x11\xaa')  # 0xf17911aa
        data.write(b'\x00\x10')  # size
        self.unselected_visor_beam_color.to_stream(data)

        data.write(b'\xa1L\x8d ')  # 0xa14c8d20
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_filled_color.to_stream(data)

        data.write(b'\xb4\x13\\\xdd')  # 0xb4135cdd
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_shadow_color.to_stream(data)

        data.write(b'\xe0)\x0cH')  # 0xe0290c48
        data.write(b'\x00\x10')  # size
        self.energy_bar_low_empty_color.to_stream(data)

        data.write(b'\x1e\xc7\xf8c')  # 0x1ec7f863
        data.write(b'\x00\x10')  # size
        self.hud_damage_modulate_color.to_stream(data)

        data.write(b'\xae\x13\x17\xd8')  # 0xae1317d8
        data.write(b'\x00\x10')  # size
        self.damage_indicator_color.to_stream(data)

        data.write(b'"\xb9\xb0\x1e')  # 0x22b9b01e
        data.write(b'\x00\x10')  # size
        self.hud_title_foreground_color.to_stream(data)

        data.write(b'p\xa2\xcdn')  # 0x70a2cd6e
        data.write(b'\x00\x10')  # size
        self.hud_title_outline_color.to_stream(data)

        data.write(b'\xe7\x07\x032')  # 0xe7070332
        data.write(b'\x00\x10')  # size
        self.unknown_0xe7070332.to_stream(data)

        data.write(b'w\x9c{\x9c')  # 0x779c7b9c
        data.write(b'\x00\x10')  # size
        self.unknown_0x779c7b9c.to_stream(data)

        data.write(b'on\x9dm')  # 0x6f6e9d6d
        data.write(b'\x00\x10')  # size
        self.energy_warning_color.to_stream(data)

        data.write(b'\x0c\x00\xa2\x9f')  # 0xc00a29f
        data.write(b'\x00\x10')  # size
        self.missile_warning_color.to_stream(data)

        data.write(b'\x83\x04\x015')  # 0x83040135
        data.write(b'\x00\x10')  # size
        self.unknown_0x83040135.to_stream(data)

        data.write(b'<\x1a\xe0\xff')  # 0x3c1ae0ff
        data.write(b'\x00\x10')  # size
        self.unknown_0x3c1ae0ff.to_stream(data)

        data.write(b')E1\x02')  # 0x29453102
        data.write(b'\x00\x10')  # size
        self.missile_bar_shadow_color.to_stream(data)

        data.write(b'd3|\xcd')  # 0x64337ccd
        data.write(b'\x00\x10')  # size
        self.missile_bar_empty_color.to_stream(data)

        data.write(b'\xbe<)\xa1')  # 0xbe3c29a1
        data.write(b'\x00\x10')  # size
        self.unknown_0xbe3c29a1.to_stream(data)

        data.write(b'\xd1\x10\xa1/')  # 0xd110a12f
        data.write(b'\x00\x10')  # size
        self.missile_group_inactive_color.to_stream(data)

        data.write(b'\xce\xb1|\xdf')  # 0xceb17cdf
        data.write(b'\x00\x10')  # size
        self.missile_group_combo_charge_color.to_stream(data)

        data.write(b'LZ\xffO')  # 0x4c5aff4f
        data.write(b'\x00\x10')  # size
        self.unknown_0x4c5aff4f.to_stream(data)

        data.write(b'\x0b\x17\xb6\x93')  # 0xb17b693
        data.write(b'\x00\x10')  # size
        self.unknown_0x0b17b693.to_stream(data)

        data.write(b'\x8b\nL\x90')  # 0x8b0a4c90
        data.write(b'\x00\x10')  # size
        self.unknown_0x8b0a4c90.to_stream(data)

        data.write(b'\xc4\xe1|\xa8')  # 0xc4e17ca8
        data.write(b'\x00\x10')  # size
        self.energy_warning_outline_color.to_stream(data)

        data.write(b'\xcd\xbds\xe1')  # 0xcdbd73e1
        data.write(b'\x00\x10')  # size
        self.missile_warning_outline_color.to_stream(data)

        data.write(b'xR$a')  # 0x78522461
        data.write(b'\x00\x10')  # size
        self.unknown_0x78522461.to_stream(data)

        data.write(b'j\x83\x9a\x97')  # 0x6a839a97
        data.write(b'\x00\x10')  # size
        self.flash_pass_color.to_stream(data)

        data.write(b'y\xeao\x12')  # 0x79ea6f12
        data.write(b'\x00\x10')  # size
        self.unknown_0x79ea6f12.to_stream(data)

        data.write(b'\xdc\x90\x12\x06')  # 0xdc901206
        data.write(b'\x00\x10')  # size
        self.unknown_0xdc901206.to_stream(data)

        data.write(b'\xc5O\xa7\xbc')  # 0xc54fa7bc
        data.write(b'\x00\x10')  # size
        self.unknown_0xc54fa7bc.to_stream(data)

        data.write(b'\x18q\x7f\xa7')  # 0x18717fa7
        data.write(b'\x00\x10')  # size
        self.unknown_0x18717fa7.to_stream(data)

        data.write(b'\x8b}sx')  # 0x8b7d7378
        data.write(b'\x00\x10')  # size
        self.unknown_0x8b7d7378.to_stream(data)

        data.write(b'\x86{\x01\xa2')  # 0x867b01a2
        data.write(b'\x00\x10')  # size
        self.unknown_0x867b01a2.to_stream(data)

        data.write(b'\xc0.\xedy')  # 0xc02eed79
        data.write(b'\x00\x10')  # size
        self.unknown_0xc02eed79.to_stream(data)

        data.write(b'\xe4\xc1\xbb\xeb')  # 0xe4c1bbeb
        data.write(b'\x00\x10')  # size
        self.metroid_suck_pulse_color.to_stream(data)

        data.write(b'\xce|\x9d\x8d')  # 0xce7c9d8d
        data.write(b'\x00\x10')  # size
        self.unknown_0xce7c9d8d.to_stream(data)

        data.write(b'\x13I\x04 ')  # 0x13490420
        data.write(b'\x00\x10')  # size
        self.energy_bar_damage_color.to_stream(data)

        data.write(b'\xaf\xe2\xd4]')  # 0xafe2d45d
        data.write(b'\x00\x10')  # size
        self.unknown_0xafe2d45d.to_stream(data)

        data.write(b'*\xf5\xaa\x06')  # 0x2af5aa06
        data.write(b'\x00\x10')  # size
        self.x_ray_holo_grid_color.to_stream(data)

        data.write(b'\xd3\xcb\xe8F')  # 0xd3cbe846
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_color.to_stream(data)

        data.write(b'P{Q\xda')  # 0x507b51da
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_ticks_color.to_stream(data)

        data.write(b'\xc6\x1d\x97\xef')  # 0xc61d97ef
        data.write(b'\x00\x10')  # size
        self.x_ray_seeker_ticks_outer_color.to_stream(data)

        data.write(b'\xaf\x00\x01\xcf')  # 0xaf0001cf
        data.write(b'\x00\x10')  # size
        self.x_ray_top_puzzle_color.to_stream(data)

        data.write(b'\x15\n\x9b\x17')  # 0x150a9b17
        data.write(b'\x00\x10')  # size
        self.x_ray_bottom_puzzle_color.to_stream(data)

        data.write(b'\xd6mq_')  # 0xd66d715f
        data.write(b'\x00\x10')  # size
        self.x_ray_left_puzzle_color.to_stream(data)

        data.write(b'\xa8i\x8f\xe8')  # 0xa8698fe8
        data.write(b'\x00\x10')  # size
        self.x_ray_right_puzzle_color.to_stream(data)

        data.write(b'L\xb3\x8eq')  # 0x4cb38e71
        data.write(b'\x00\x10')  # size
        self.x_ray_corner_color.to_stream(data)

        data.write(b'\xa9G\xa6|')  # 0xa947a67c
        data.write(b'\x00\x10')  # size
        self.unknown_0xa947a67c.to_stream(data)

        data.write(b'B\x1b\xae*')  # 0x421bae2a
        data.write(b'\x00\x10')  # size
        self.unknown_0x421bae2a.to_stream(data)

        data.write(b'C\x9a7t')  # 0x439a3774
        data.write(b'\x00\x10')  # size
        self.unknown_0x439a3774.to_stream(data)

        data.write(b'\x8e\xe9L\x81')  # 0x8ee94c81
        data.write(b'\x00\x10')  # size
        self.unknown_0x8ee94c81.to_stream(data)

        data.write(b'qnc\x98')  # 0x716e6398
        data.write(b'\x00\x10')  # size
        self.unknown_0x716e6398.to_stream(data)

        data.write(b'\xda\xcaF\xd4')  # 0xdaca46d4
        data.write(b'\x00\x10')  # size
        self.steam_no_blur_color.to_stream(data)

        data.write(b'\x0f7\xe7V')  # 0xf37e756
        data.write(b'\x00\x10')  # size
        self.unknown_0x0f37e756.to_stream(data)

        data.write(b'\xf7(6D')  # 0xf7283644
        data.write(b'\x00\x10')  # size
        self.unknown_0xf7283644.to_stream(data)

        data.write(b'7VK}')  # 0x37564b7d
        data.write(b'\x00\x10')  # size
        self.unknown_0x37564b7d.to_stream(data)

        data.write(b'f\xb7\xed\xa3')  # 0x66b7eda3
        data.write(b'\x00\x10')  # size
        self.unknown_0x66b7eda3.to_stream(data)

        data.write(b'\xf8\x95\t\x8f')  # 0xf895098f
        data.write(b'\x00\x10')  # size
        self.unknown_0xf895098f.to_stream(data)

        data.write(b"\x9b'\xbe\x10")  # 0x9b27be10
        data.write(b'\x00\x10')  # size
        self.unknown_0x9b27be10.to_stream(data)

        data.write(b'l\x85P\xc9')  # 0x6c8550c9
        data.write(b'\x00\x10')  # size
        self.unknown_0x6c8550c9.to_stream(data)

        data.write(b'Sh\xa3_')  # 0x5368a35f
        data.write(b'\x00\x10')  # size
        self.unknown_0x5368a35f.to_stream(data)

        data.write(b'Z\x80{\x81')  # 0x5a807b81
        data.write(b'\x00\x10')  # size
        self.unknown_0x5a807b81.to_stream(data)

        data.write(b'\xebc\xaf\xed')  # 0xeb63afed
        data.write(b'\x00\x10')  # size
        self.unknown_0xeb63afed.to_stream(data)

        data.write(b'\xab\xdb\xfa[')  # 0xabdbfa5b
        data.write(b'\x00\x10')  # size
        self.scan_images_color.to_stream(data)

        data.write(b'\xd3\xba\xfa\xf5')  # 0xd3bafaf5
        data.write(b'\x00\x10')  # size
        self.unknown_0xd3bafaf5.to_stream(data)

        data.write(b'\xf8\xb9q\xfa')  # 0xf8b971fa
        data.write(b'\x00\x10')  # size
        self.threat_group_damage_color.to_stream(data)

        data.write(b'O\x1dD>')  # 0x4f1d443e
        data.write(b'\x00\x10')  # size
        self.unknown_0x4f1d443e.to_stream(data)

        data.write(b'\x0fdQ\xda')  # 0xf6451da
        data.write(b'\x00\x10')  # size
        self.unknown_0x0f6451da.to_stream(data)

        data.write(b'4^[N')  # 0x345e5b4e
        data.write(b'\x00\x10')  # size
        self.scan_seeker_color.to_stream(data)

        data.write(b'C\xed3\x10')  # 0x43ed3310
        data.write(b'\x00\x10')  # size
        self.unknown_0x43ed3310.to_stream(data)

        data.write(b'\xa7\x81\xed\x1d')  # 0xa781ed1d
        data.write(b'\x00\x10')  # size
        self.unknown_0xa781ed1d.to_stream(data)

        data.write(b'\x1b\x0f:\x85')  # 0x1b0f3a85
        data.write(b'\x00\x10')  # size
        self.log_book_color.to_stream(data)

        data.write(b'\xebZ\xe6e')  # 0xeb5ae665
        data.write(b'\x00\x10')  # size
        self.log_book_frame_color.to_stream(data)

        data.write(b'\x14\x93i\xfd')  # 0x149369fd
        data.write(b'\x00\x10')  # size
        self.inventory_equipped_color.to_stream(data)

        data.write(b'e\xee\x03\xa7')  # 0x65ee03a7
        data.write(b'\x00\x10')  # size
        self.command_text_color.to_stream(data)

        data.write(b'U\xbb\x9b\xa8')  # 0x55bb9ba8
        data.write(b'\x00\x10')  # size
        self.command_text_outline_color.to_stream(data)

        data.write(b'K\x03\xe78')  # 0x4b03e738
        data.write(b'\x00\x10')  # size
        self.unknown_0x4b03e738.to_stream(data)

        data.write(b'\xf8\x83`|')  # 0xf883607c
        data.write(b'\x00\x10')  # size
        self.unknown_0xf883607c.to_stream(data)

        data.write(b'\xb6\x8f\x96\xec')  # 0xb68f96ec
        data.write(b'\x00\x10')  # size
        self.unknown_0xb68f96ec.to_stream(data)

        data.write(b'.sT\x9a')  # 0x2e73549a
        data.write(b'\x00\x10')  # size
        self.unknown_0x2e73549a.to_stream(data)

        data.write(b'\x93\x8f:\xf5')  # 0x938f3af5
        data.write(b'\x00\x10')  # size
        self.unknown_0x938f3af5.to_stream(data)

        data.write(b"?'\xfa\x9a")  # 0x3f27fa9a
        data.write(b'\x00\x10')  # size
        self.unknown_0x3f27fa9a.to_stream(data)

        data.write(b'\xd2\xfav1')  # 0xd2fa7631
        data.write(b'\x00\x10')  # size
        self.unknown_0xd2fa7631.to_stream(data)

        data.write(b'\xdf\xcf\x84\xe1')  # 0xdfcf84e1
        data.write(b'\x00\x10')  # size
        self.unknown_0xdfcf84e1.to_stream(data)

        data.write(b'\x16\x91,\xa9')  # 0x16912ca9
        data.write(b'\x00\x10')  # size
        self.unknown_0x16912ca9.to_stream(data)

        data.write(b'\xe5\x0c\xdaR')  # 0xe50cda52
        data.write(b'\x00\x10')  # size
        self.unknown_0xe50cda52.to_stream(data)

        data.write(b'}\xc0v\xa6')  # 0x7dc076a6
        data.write(b'\x00\x10')  # size
        self.unknown_0x7dc076a6.to_stream(data)

        data.write(b'\xc6\xf8k\xfd')  # 0xc6f86bfd
        data.write(b'\x00\x10')  # size
        self.unknown_0xc6f86bfd.to_stream(data)

        data.write(b'\xbf\xff\xe9Z')  # 0xbfffe95a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbfffe95a))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x8ed04c36=Color.from_json(data['unknown_0x8ed04c36']),
            unknown_0x94bb7ee5=Color.from_json(data['unknown_0x94bb7ee5']),
            pause_screen_tweak_open_color=Color.from_json(data['pause_screen_tweak_open_color']),
            unknown_0x415a81f8=Color.from_json(data['unknown_0x415a81f8']),
            unknown_0xfe95100f=Color.from_json(data['unknown_0xfe95100f']),
            pause_screen_fullscreen_bg_color=Color.from_json(data['pause_screen_fullscreen_bg_color']),
            unknown_0x66733e29=Color.from_json(data['unknown_0x66733e29']),
            pause_screen_frame_color=Color.from_json(data['pause_screen_frame_color']),
            pause_screen_icons_color=Color.from_json(data['pause_screen_icons_color']),
            pause_screen_text_color=Color.from_json(data['pause_screen_text_color']),
            pause_screen_highlight_color=Color.from_json(data['pause_screen_highlight_color']),
            pause_screen_helmet_color=Color.from_json(data['pause_screen_helmet_color']),
            gui_cursor_color=Color.from_json(data['gui_cursor_color']),
            unknown_0xdb5c8a60=Color.from_json(data['unknown_0xdb5c8a60']),
            unknown_0x166c22e0=Color.from_json(data['unknown_0x166c22e0']),
            unknown_0xcec78e81=Color.from_json(data['unknown_0xcec78e81']),
            unknown_0x91338f72=Color.from_json(data['unknown_0x91338f72']),
            hud_memo_text_foreground_color=Color.from_json(data['hud_memo_text_foreground_color']),
            hud_memo_text_outline_color=Color.from_json(data['hud_memo_text_outline_color']),
            unknown_0xc8ddc662=Color.from_json(data['unknown_0xc8ddc662']),
            hud_glow_color=Color.from_json(data['hud_glow_color']),
            unknown_0x5c336f85=Color.from_json(data['unknown_0x5c336f85']),
            unknown_0xdefca700=Color.from_json(data['unknown_0xdefca700']),
            selected_visor_beam_color=Color.from_json(data['selected_visor_beam_color']),
            unselected_visor_beam_color=Color.from_json(data['unselected_visor_beam_color']),
            energy_bar_low_filled_color=Color.from_json(data['energy_bar_low_filled_color']),
            energy_bar_low_shadow_color=Color.from_json(data['energy_bar_low_shadow_color']),
            energy_bar_low_empty_color=Color.from_json(data['energy_bar_low_empty_color']),
            hud_damage_modulate_color=Color.from_json(data['hud_damage_modulate_color']),
            damage_indicator_color=Color.from_json(data['damage_indicator_color']),
            hud_title_foreground_color=Color.from_json(data['hud_title_foreground_color']),
            hud_title_outline_color=Color.from_json(data['hud_title_outline_color']),
            unknown_0xe7070332=Color.from_json(data['unknown_0xe7070332']),
            unknown_0x779c7b9c=Color.from_json(data['unknown_0x779c7b9c']),
            energy_warning_color=Color.from_json(data['energy_warning_color']),
            missile_warning_color=Color.from_json(data['missile_warning_color']),
            unknown_0x83040135=Color.from_json(data['unknown_0x83040135']),
            unknown_0x3c1ae0ff=Color.from_json(data['unknown_0x3c1ae0ff']),
            missile_bar_shadow_color=Color.from_json(data['missile_bar_shadow_color']),
            missile_bar_empty_color=Color.from_json(data['missile_bar_empty_color']),
            unknown_0xbe3c29a1=Color.from_json(data['unknown_0xbe3c29a1']),
            missile_group_inactive_color=Color.from_json(data['missile_group_inactive_color']),
            missile_group_combo_charge_color=Color.from_json(data['missile_group_combo_charge_color']),
            unknown_0x4c5aff4f=Color.from_json(data['unknown_0x4c5aff4f']),
            unknown_0x0b17b693=Color.from_json(data['unknown_0x0b17b693']),
            unknown_0x8b0a4c90=Color.from_json(data['unknown_0x8b0a4c90']),
            energy_warning_outline_color=Color.from_json(data['energy_warning_outline_color']),
            missile_warning_outline_color=Color.from_json(data['missile_warning_outline_color']),
            unknown_0x78522461=Color.from_json(data['unknown_0x78522461']),
            flash_pass_color=Color.from_json(data['flash_pass_color']),
            unknown_0x79ea6f12=Color.from_json(data['unknown_0x79ea6f12']),
            unknown_0xdc901206=Color.from_json(data['unknown_0xdc901206']),
            unknown_0xc54fa7bc=Color.from_json(data['unknown_0xc54fa7bc']),
            unknown_0x18717fa7=Color.from_json(data['unknown_0x18717fa7']),
            unknown_0x8b7d7378=Color.from_json(data['unknown_0x8b7d7378']),
            unknown_0x867b01a2=Color.from_json(data['unknown_0x867b01a2']),
            unknown_0xc02eed79=Color.from_json(data['unknown_0xc02eed79']),
            metroid_suck_pulse_color=Color.from_json(data['metroid_suck_pulse_color']),
            unknown_0xce7c9d8d=Color.from_json(data['unknown_0xce7c9d8d']),
            energy_bar_damage_color=Color.from_json(data['energy_bar_damage_color']),
            unknown_0xafe2d45d=Color.from_json(data['unknown_0xafe2d45d']),
            x_ray_holo_grid_color=Color.from_json(data['x_ray_holo_grid_color']),
            x_ray_seeker_color=Color.from_json(data['x_ray_seeker_color']),
            x_ray_seeker_ticks_color=Color.from_json(data['x_ray_seeker_ticks_color']),
            x_ray_seeker_ticks_outer_color=Color.from_json(data['x_ray_seeker_ticks_outer_color']),
            x_ray_top_puzzle_color=Color.from_json(data['x_ray_top_puzzle_color']),
            x_ray_bottom_puzzle_color=Color.from_json(data['x_ray_bottom_puzzle_color']),
            x_ray_left_puzzle_color=Color.from_json(data['x_ray_left_puzzle_color']),
            x_ray_right_puzzle_color=Color.from_json(data['x_ray_right_puzzle_color']),
            x_ray_corner_color=Color.from_json(data['x_ray_corner_color']),
            unknown_0xa947a67c=Color.from_json(data['unknown_0xa947a67c']),
            unknown_0x421bae2a=Color.from_json(data['unknown_0x421bae2a']),
            unknown_0x439a3774=Color.from_json(data['unknown_0x439a3774']),
            unknown_0x8ee94c81=Color.from_json(data['unknown_0x8ee94c81']),
            unknown_0x716e6398=Color.from_json(data['unknown_0x716e6398']),
            steam_no_blur_color=Color.from_json(data['steam_no_blur_color']),
            unknown_0x0f37e756=Color.from_json(data['unknown_0x0f37e756']),
            unknown_0xf7283644=Color.from_json(data['unknown_0xf7283644']),
            unknown_0x37564b7d=Color.from_json(data['unknown_0x37564b7d']),
            unknown_0x66b7eda3=Color.from_json(data['unknown_0x66b7eda3']),
            unknown_0xf895098f=Color.from_json(data['unknown_0xf895098f']),
            unknown_0x9b27be10=Color.from_json(data['unknown_0x9b27be10']),
            unknown_0x6c8550c9=Color.from_json(data['unknown_0x6c8550c9']),
            unknown_0x5368a35f=Color.from_json(data['unknown_0x5368a35f']),
            unknown_0x5a807b81=Color.from_json(data['unknown_0x5a807b81']),
            unknown_0xeb63afed=Color.from_json(data['unknown_0xeb63afed']),
            scan_images_color=Color.from_json(data['scan_images_color']),
            unknown_0xd3bafaf5=Color.from_json(data['unknown_0xd3bafaf5']),
            threat_group_damage_color=Color.from_json(data['threat_group_damage_color']),
            unknown_0x4f1d443e=Color.from_json(data['unknown_0x4f1d443e']),
            unknown_0x0f6451da=Color.from_json(data['unknown_0x0f6451da']),
            scan_seeker_color=Color.from_json(data['scan_seeker_color']),
            unknown_0x43ed3310=Color.from_json(data['unknown_0x43ed3310']),
            unknown_0xa781ed1d=Color.from_json(data['unknown_0xa781ed1d']),
            log_book_color=Color.from_json(data['log_book_color']),
            log_book_frame_color=Color.from_json(data['log_book_frame_color']),
            inventory_equipped_color=Color.from_json(data['inventory_equipped_color']),
            command_text_color=Color.from_json(data['command_text_color']),
            command_text_outline_color=Color.from_json(data['command_text_outline_color']),
            unknown_0x4b03e738=Color.from_json(data['unknown_0x4b03e738']),
            unknown_0xf883607c=Color.from_json(data['unknown_0xf883607c']),
            unknown_0xb68f96ec=Color.from_json(data['unknown_0xb68f96ec']),
            unknown_0x2e73549a=Color.from_json(data['unknown_0x2e73549a']),
            unknown_0x938f3af5=Color.from_json(data['unknown_0x938f3af5']),
            unknown_0x3f27fa9a=Color.from_json(data['unknown_0x3f27fa9a']),
            unknown_0xd2fa7631=Color.from_json(data['unknown_0xd2fa7631']),
            unknown_0xdfcf84e1=Color.from_json(data['unknown_0xdfcf84e1']),
            unknown_0x16912ca9=Color.from_json(data['unknown_0x16912ca9']),
            unknown_0xe50cda52=Color.from_json(data['unknown_0xe50cda52']),
            unknown_0x7dc076a6=Color.from_json(data['unknown_0x7dc076a6']),
            unknown_0xc6f86bfd=Color.from_json(data['unknown_0xc6f86bfd']),
            unknown_0xbfffe95a=data['unknown_0xbfffe95a'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x8ed04c36': self.unknown_0x8ed04c36.to_json(),
            'unknown_0x94bb7ee5': self.unknown_0x94bb7ee5.to_json(),
            'pause_screen_tweak_open_color': self.pause_screen_tweak_open_color.to_json(),
            'unknown_0x415a81f8': self.unknown_0x415a81f8.to_json(),
            'unknown_0xfe95100f': self.unknown_0xfe95100f.to_json(),
            'pause_screen_fullscreen_bg_color': self.pause_screen_fullscreen_bg_color.to_json(),
            'unknown_0x66733e29': self.unknown_0x66733e29.to_json(),
            'pause_screen_frame_color': self.pause_screen_frame_color.to_json(),
            'pause_screen_icons_color': self.pause_screen_icons_color.to_json(),
            'pause_screen_text_color': self.pause_screen_text_color.to_json(),
            'pause_screen_highlight_color': self.pause_screen_highlight_color.to_json(),
            'pause_screen_helmet_color': self.pause_screen_helmet_color.to_json(),
            'gui_cursor_color': self.gui_cursor_color.to_json(),
            'unknown_0xdb5c8a60': self.unknown_0xdb5c8a60.to_json(),
            'unknown_0x166c22e0': self.unknown_0x166c22e0.to_json(),
            'unknown_0xcec78e81': self.unknown_0xcec78e81.to_json(),
            'unknown_0x91338f72': self.unknown_0x91338f72.to_json(),
            'hud_memo_text_foreground_color': self.hud_memo_text_foreground_color.to_json(),
            'hud_memo_text_outline_color': self.hud_memo_text_outline_color.to_json(),
            'unknown_0xc8ddc662': self.unknown_0xc8ddc662.to_json(),
            'hud_glow_color': self.hud_glow_color.to_json(),
            'unknown_0x5c336f85': self.unknown_0x5c336f85.to_json(),
            'unknown_0xdefca700': self.unknown_0xdefca700.to_json(),
            'selected_visor_beam_color': self.selected_visor_beam_color.to_json(),
            'unselected_visor_beam_color': self.unselected_visor_beam_color.to_json(),
            'energy_bar_low_filled_color': self.energy_bar_low_filled_color.to_json(),
            'energy_bar_low_shadow_color': self.energy_bar_low_shadow_color.to_json(),
            'energy_bar_low_empty_color': self.energy_bar_low_empty_color.to_json(),
            'hud_damage_modulate_color': self.hud_damage_modulate_color.to_json(),
            'damage_indicator_color': self.damage_indicator_color.to_json(),
            'hud_title_foreground_color': self.hud_title_foreground_color.to_json(),
            'hud_title_outline_color': self.hud_title_outline_color.to_json(),
            'unknown_0xe7070332': self.unknown_0xe7070332.to_json(),
            'unknown_0x779c7b9c': self.unknown_0x779c7b9c.to_json(),
            'energy_warning_color': self.energy_warning_color.to_json(),
            'missile_warning_color': self.missile_warning_color.to_json(),
            'unknown_0x83040135': self.unknown_0x83040135.to_json(),
            'unknown_0x3c1ae0ff': self.unknown_0x3c1ae0ff.to_json(),
            'missile_bar_shadow_color': self.missile_bar_shadow_color.to_json(),
            'missile_bar_empty_color': self.missile_bar_empty_color.to_json(),
            'unknown_0xbe3c29a1': self.unknown_0xbe3c29a1.to_json(),
            'missile_group_inactive_color': self.missile_group_inactive_color.to_json(),
            'missile_group_combo_charge_color': self.missile_group_combo_charge_color.to_json(),
            'unknown_0x4c5aff4f': self.unknown_0x4c5aff4f.to_json(),
            'unknown_0x0b17b693': self.unknown_0x0b17b693.to_json(),
            'unknown_0x8b0a4c90': self.unknown_0x8b0a4c90.to_json(),
            'energy_warning_outline_color': self.energy_warning_outline_color.to_json(),
            'missile_warning_outline_color': self.missile_warning_outline_color.to_json(),
            'unknown_0x78522461': self.unknown_0x78522461.to_json(),
            'flash_pass_color': self.flash_pass_color.to_json(),
            'unknown_0x79ea6f12': self.unknown_0x79ea6f12.to_json(),
            'unknown_0xdc901206': self.unknown_0xdc901206.to_json(),
            'unknown_0xc54fa7bc': self.unknown_0xc54fa7bc.to_json(),
            'unknown_0x18717fa7': self.unknown_0x18717fa7.to_json(),
            'unknown_0x8b7d7378': self.unknown_0x8b7d7378.to_json(),
            'unknown_0x867b01a2': self.unknown_0x867b01a2.to_json(),
            'unknown_0xc02eed79': self.unknown_0xc02eed79.to_json(),
            'metroid_suck_pulse_color': self.metroid_suck_pulse_color.to_json(),
            'unknown_0xce7c9d8d': self.unknown_0xce7c9d8d.to_json(),
            'energy_bar_damage_color': self.energy_bar_damage_color.to_json(),
            'unknown_0xafe2d45d': self.unknown_0xafe2d45d.to_json(),
            'x_ray_holo_grid_color': self.x_ray_holo_grid_color.to_json(),
            'x_ray_seeker_color': self.x_ray_seeker_color.to_json(),
            'x_ray_seeker_ticks_color': self.x_ray_seeker_ticks_color.to_json(),
            'x_ray_seeker_ticks_outer_color': self.x_ray_seeker_ticks_outer_color.to_json(),
            'x_ray_top_puzzle_color': self.x_ray_top_puzzle_color.to_json(),
            'x_ray_bottom_puzzle_color': self.x_ray_bottom_puzzle_color.to_json(),
            'x_ray_left_puzzle_color': self.x_ray_left_puzzle_color.to_json(),
            'x_ray_right_puzzle_color': self.x_ray_right_puzzle_color.to_json(),
            'x_ray_corner_color': self.x_ray_corner_color.to_json(),
            'unknown_0xa947a67c': self.unknown_0xa947a67c.to_json(),
            'unknown_0x421bae2a': self.unknown_0x421bae2a.to_json(),
            'unknown_0x439a3774': self.unknown_0x439a3774.to_json(),
            'unknown_0x8ee94c81': self.unknown_0x8ee94c81.to_json(),
            'unknown_0x716e6398': self.unknown_0x716e6398.to_json(),
            'steam_no_blur_color': self.steam_no_blur_color.to_json(),
            'unknown_0x0f37e756': self.unknown_0x0f37e756.to_json(),
            'unknown_0xf7283644': self.unknown_0xf7283644.to_json(),
            'unknown_0x37564b7d': self.unknown_0x37564b7d.to_json(),
            'unknown_0x66b7eda3': self.unknown_0x66b7eda3.to_json(),
            'unknown_0xf895098f': self.unknown_0xf895098f.to_json(),
            'unknown_0x9b27be10': self.unknown_0x9b27be10.to_json(),
            'unknown_0x6c8550c9': self.unknown_0x6c8550c9.to_json(),
            'unknown_0x5368a35f': self.unknown_0x5368a35f.to_json(),
            'unknown_0x5a807b81': self.unknown_0x5a807b81.to_json(),
            'unknown_0xeb63afed': self.unknown_0xeb63afed.to_json(),
            'scan_images_color': self.scan_images_color.to_json(),
            'unknown_0xd3bafaf5': self.unknown_0xd3bafaf5.to_json(),
            'threat_group_damage_color': self.threat_group_damage_color.to_json(),
            'unknown_0x4f1d443e': self.unknown_0x4f1d443e.to_json(),
            'unknown_0x0f6451da': self.unknown_0x0f6451da.to_json(),
            'scan_seeker_color': self.scan_seeker_color.to_json(),
            'unknown_0x43ed3310': self.unknown_0x43ed3310.to_json(),
            'unknown_0xa781ed1d': self.unknown_0xa781ed1d.to_json(),
            'log_book_color': self.log_book_color.to_json(),
            'log_book_frame_color': self.log_book_frame_color.to_json(),
            'inventory_equipped_color': self.inventory_equipped_color.to_json(),
            'command_text_color': self.command_text_color.to_json(),
            'command_text_outline_color': self.command_text_outline_color.to_json(),
            'unknown_0x4b03e738': self.unknown_0x4b03e738.to_json(),
            'unknown_0xf883607c': self.unknown_0xf883607c.to_json(),
            'unknown_0xb68f96ec': self.unknown_0xb68f96ec.to_json(),
            'unknown_0x2e73549a': self.unknown_0x2e73549a.to_json(),
            'unknown_0x938f3af5': self.unknown_0x938f3af5.to_json(),
            'unknown_0x3f27fa9a': self.unknown_0x3f27fa9a.to_json(),
            'unknown_0xd2fa7631': self.unknown_0xd2fa7631.to_json(),
            'unknown_0xdfcf84e1': self.unknown_0xdfcf84e1.to_json(),
            'unknown_0x16912ca9': self.unknown_0x16912ca9.to_json(),
            'unknown_0xe50cda52': self.unknown_0xe50cda52.to_json(),
            'unknown_0x7dc076a6': self.unknown_0x7dc076a6.to_json(),
            'unknown_0xc6f86bfd': self.unknown_0xc6f86bfd.to_json(),
            'unknown_0xbfffe95a': self.unknown_0xbfffe95a,
        }


def _decode_unknown_0x8ed04c36(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x94bb7ee5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_tweak_open_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x415a81f8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xfe95100f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_fullscreen_bg_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x66733e29(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_frame_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_icons_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_text_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_highlight_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_pause_screen_helmet_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gui_cursor_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdb5c8a60(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x166c22e0(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xcec78e81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x91338f72(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_memo_text_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_memo_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc8ddc662(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_glow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5c336f85(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdefca700(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_selected_visor_beam_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unselected_visor_beam_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_filled_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_low_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_damage_modulate_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_damage_indicator_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_title_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_hud_title_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe7070332(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x779c7b9c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_warning_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_warning_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x83040135(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3c1ae0ff(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_bar_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_bar_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xbe3c29a1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_combo_charge_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4c5aff4f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0b17b693(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8b0a4c90(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_warning_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_warning_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x78522461(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_flash_pass_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x79ea6f12(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdc901206(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc54fa7bc(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x18717fa7(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8b7d7378(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x867b01a2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc02eed79(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_metroid_suck_pulse_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xce7c9d8d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_damage_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xafe2d45d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_holo_grid_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_ticks_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_seeker_ticks_outer_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_top_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_bottom_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_left_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_right_puzzle_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_x_ray_corner_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa947a67c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x421bae2a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x439a3774(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x8ee94c81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x716e6398(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_steam_no_blur_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0f37e756(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf7283644(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x37564b7d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x66b7eda3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf895098f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x9b27be10(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x6c8550c9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5368a35f(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x5a807b81(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xeb63afed(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_images_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xd3bafaf5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_damage_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4f1d443e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x0f6451da(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_scan_seeker_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x43ed3310(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa781ed1d(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_log_book_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_log_book_frame_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_inventory_equipped_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_command_text_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_command_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x4b03e738(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xf883607c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb68f96ec(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x2e73549a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x938f3af5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x3f27fa9a(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xd2fa7631(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdfcf84e1(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x16912ca9(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe50cda52(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x7dc076a6(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xc6f86bfd(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xbfffe95a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8ed04c36: ('unknown_0x8ed04c36', _decode_unknown_0x8ed04c36),
    0x94bb7ee5: ('unknown_0x94bb7ee5', _decode_unknown_0x94bb7ee5),
    0x2d037b5a: ('pause_screen_tweak_open_color', _decode_pause_screen_tweak_open_color),
    0x415a81f8: ('unknown_0x415a81f8', _decode_unknown_0x415a81f8),
    0xfe95100f: ('unknown_0xfe95100f', _decode_unknown_0xfe95100f),
    0xaf38a796: ('pause_screen_fullscreen_bg_color', _decode_pause_screen_fullscreen_bg_color),
    0x66733e29: ('unknown_0x66733e29', _decode_unknown_0x66733e29),
    0xff6d31e9: ('pause_screen_frame_color', _decode_pause_screen_frame_color),
    0x9b63ffa6: ('pause_screen_icons_color', _decode_pause_screen_icons_color),
    0x7298e223: ('pause_screen_text_color', _decode_pause_screen_text_color),
    0x556481e8: ('pause_screen_highlight_color', _decode_pause_screen_highlight_color),
    0xee8a2117: ('pause_screen_helmet_color', _decode_pause_screen_helmet_color),
    0xf468695d: ('gui_cursor_color', _decode_gui_cursor_color),
    0xdb5c8a60: ('unknown_0xdb5c8a60', _decode_unknown_0xdb5c8a60),
    0x166c22e0: ('unknown_0x166c22e0', _decode_unknown_0x166c22e0),
    0xcec78e81: ('unknown_0xcec78e81', _decode_unknown_0xcec78e81),
    0x91338f72: ('unknown_0x91338f72', _decode_unknown_0x91338f72),
    0x2df1eb03: ('hud_memo_text_foreground_color', _decode_hud_memo_text_foreground_color),
    0xb5da30f4: ('hud_memo_text_outline_color', _decode_hud_memo_text_outline_color),
    0xc8ddc662: ('unknown_0xc8ddc662', _decode_unknown_0xc8ddc662),
    0x6991e2cd: ('hud_glow_color', _decode_hud_glow_color),
    0x5c336f85: ('unknown_0x5c336f85', _decode_unknown_0x5c336f85),
    0xdefca700: ('unknown_0xdefca700', _decode_unknown_0xdefca700),
    0xcb7ddaf4: ('selected_visor_beam_color', _decode_selected_visor_beam_color),
    0xf17911aa: ('unselected_visor_beam_color', _decode_unselected_visor_beam_color),
    0xa14c8d20: ('energy_bar_low_filled_color', _decode_energy_bar_low_filled_color),
    0xb4135cdd: ('energy_bar_low_shadow_color', _decode_energy_bar_low_shadow_color),
    0xe0290c48: ('energy_bar_low_empty_color', _decode_energy_bar_low_empty_color),
    0x1ec7f863: ('hud_damage_modulate_color', _decode_hud_damage_modulate_color),
    0xae1317d8: ('damage_indicator_color', _decode_damage_indicator_color),
    0x22b9b01e: ('hud_title_foreground_color', _decode_hud_title_foreground_color),
    0x70a2cd6e: ('hud_title_outline_color', _decode_hud_title_outline_color),
    0xe7070332: ('unknown_0xe7070332', _decode_unknown_0xe7070332),
    0x779c7b9c: ('unknown_0x779c7b9c', _decode_unknown_0x779c7b9c),
    0x6f6e9d6d: ('energy_warning_color', _decode_energy_warning_color),
    0xc00a29f: ('missile_warning_color', _decode_missile_warning_color),
    0x83040135: ('unknown_0x83040135', _decode_unknown_0x83040135),
    0x3c1ae0ff: ('unknown_0x3c1ae0ff', _decode_unknown_0x3c1ae0ff),
    0x29453102: ('missile_bar_shadow_color', _decode_missile_bar_shadow_color),
    0x64337ccd: ('missile_bar_empty_color', _decode_missile_bar_empty_color),
    0xbe3c29a1: ('unknown_0xbe3c29a1', _decode_unknown_0xbe3c29a1),
    0xd110a12f: ('missile_group_inactive_color', _decode_missile_group_inactive_color),
    0xceb17cdf: ('missile_group_combo_charge_color', _decode_missile_group_combo_charge_color),
    0x4c5aff4f: ('unknown_0x4c5aff4f', _decode_unknown_0x4c5aff4f),
    0xb17b693: ('unknown_0x0b17b693', _decode_unknown_0x0b17b693),
    0x8b0a4c90: ('unknown_0x8b0a4c90', _decode_unknown_0x8b0a4c90),
    0xc4e17ca8: ('energy_warning_outline_color', _decode_energy_warning_outline_color),
    0xcdbd73e1: ('missile_warning_outline_color', _decode_missile_warning_outline_color),
    0x78522461: ('unknown_0x78522461', _decode_unknown_0x78522461),
    0x6a839a97: ('flash_pass_color', _decode_flash_pass_color),
    0x79ea6f12: ('unknown_0x79ea6f12', _decode_unknown_0x79ea6f12),
    0xdc901206: ('unknown_0xdc901206', _decode_unknown_0xdc901206),
    0xc54fa7bc: ('unknown_0xc54fa7bc', _decode_unknown_0xc54fa7bc),
    0x18717fa7: ('unknown_0x18717fa7', _decode_unknown_0x18717fa7),
    0x8b7d7378: ('unknown_0x8b7d7378', _decode_unknown_0x8b7d7378),
    0x867b01a2: ('unknown_0x867b01a2', _decode_unknown_0x867b01a2),
    0xc02eed79: ('unknown_0xc02eed79', _decode_unknown_0xc02eed79),
    0xe4c1bbeb: ('metroid_suck_pulse_color', _decode_metroid_suck_pulse_color),
    0xce7c9d8d: ('unknown_0xce7c9d8d', _decode_unknown_0xce7c9d8d),
    0x13490420: ('energy_bar_damage_color', _decode_energy_bar_damage_color),
    0xafe2d45d: ('unknown_0xafe2d45d', _decode_unknown_0xafe2d45d),
    0x2af5aa06: ('x_ray_holo_grid_color', _decode_x_ray_holo_grid_color),
    0xd3cbe846: ('x_ray_seeker_color', _decode_x_ray_seeker_color),
    0x507b51da: ('x_ray_seeker_ticks_color', _decode_x_ray_seeker_ticks_color),
    0xc61d97ef: ('x_ray_seeker_ticks_outer_color', _decode_x_ray_seeker_ticks_outer_color),
    0xaf0001cf: ('x_ray_top_puzzle_color', _decode_x_ray_top_puzzle_color),
    0x150a9b17: ('x_ray_bottom_puzzle_color', _decode_x_ray_bottom_puzzle_color),
    0xd66d715f: ('x_ray_left_puzzle_color', _decode_x_ray_left_puzzle_color),
    0xa8698fe8: ('x_ray_right_puzzle_color', _decode_x_ray_right_puzzle_color),
    0x4cb38e71: ('x_ray_corner_color', _decode_x_ray_corner_color),
    0xa947a67c: ('unknown_0xa947a67c', _decode_unknown_0xa947a67c),
    0x421bae2a: ('unknown_0x421bae2a', _decode_unknown_0x421bae2a),
    0x439a3774: ('unknown_0x439a3774', _decode_unknown_0x439a3774),
    0x8ee94c81: ('unknown_0x8ee94c81', _decode_unknown_0x8ee94c81),
    0x716e6398: ('unknown_0x716e6398', _decode_unknown_0x716e6398),
    0xdaca46d4: ('steam_no_blur_color', _decode_steam_no_blur_color),
    0xf37e756: ('unknown_0x0f37e756', _decode_unknown_0x0f37e756),
    0xf7283644: ('unknown_0xf7283644', _decode_unknown_0xf7283644),
    0x37564b7d: ('unknown_0x37564b7d', _decode_unknown_0x37564b7d),
    0x66b7eda3: ('unknown_0x66b7eda3', _decode_unknown_0x66b7eda3),
    0xf895098f: ('unknown_0xf895098f', _decode_unknown_0xf895098f),
    0x9b27be10: ('unknown_0x9b27be10', _decode_unknown_0x9b27be10),
    0x6c8550c9: ('unknown_0x6c8550c9', _decode_unknown_0x6c8550c9),
    0x5368a35f: ('unknown_0x5368a35f', _decode_unknown_0x5368a35f),
    0x5a807b81: ('unknown_0x5a807b81', _decode_unknown_0x5a807b81),
    0xeb63afed: ('unknown_0xeb63afed', _decode_unknown_0xeb63afed),
    0xabdbfa5b: ('scan_images_color', _decode_scan_images_color),
    0xd3bafaf5: ('unknown_0xd3bafaf5', _decode_unknown_0xd3bafaf5),
    0xf8b971fa: ('threat_group_damage_color', _decode_threat_group_damage_color),
    0x4f1d443e: ('unknown_0x4f1d443e', _decode_unknown_0x4f1d443e),
    0xf6451da: ('unknown_0x0f6451da', _decode_unknown_0x0f6451da),
    0x345e5b4e: ('scan_seeker_color', _decode_scan_seeker_color),
    0x43ed3310: ('unknown_0x43ed3310', _decode_unknown_0x43ed3310),
    0xa781ed1d: ('unknown_0xa781ed1d', _decode_unknown_0xa781ed1d),
    0x1b0f3a85: ('log_book_color', _decode_log_book_color),
    0xeb5ae665: ('log_book_frame_color', _decode_log_book_frame_color),
    0x149369fd: ('inventory_equipped_color', _decode_inventory_equipped_color),
    0x65ee03a7: ('command_text_color', _decode_command_text_color),
    0x55bb9ba8: ('command_text_outline_color', _decode_command_text_outline_color),
    0x4b03e738: ('unknown_0x4b03e738', _decode_unknown_0x4b03e738),
    0xf883607c: ('unknown_0xf883607c', _decode_unknown_0xf883607c),
    0xb68f96ec: ('unknown_0xb68f96ec', _decode_unknown_0xb68f96ec),
    0x2e73549a: ('unknown_0x2e73549a', _decode_unknown_0x2e73549a),
    0x938f3af5: ('unknown_0x938f3af5', _decode_unknown_0x938f3af5),
    0x3f27fa9a: ('unknown_0x3f27fa9a', _decode_unknown_0x3f27fa9a),
    0xd2fa7631: ('unknown_0xd2fa7631', _decode_unknown_0xd2fa7631),
    0xdfcf84e1: ('unknown_0xdfcf84e1', _decode_unknown_0xdfcf84e1),
    0x16912ca9: ('unknown_0x16912ca9', _decode_unknown_0x16912ca9),
    0xe50cda52: ('unknown_0xe50cda52', _decode_unknown_0xe50cda52),
    0x7dc076a6: ('unknown_0x7dc076a6', _decode_unknown_0x7dc076a6),
    0xc6f86bfd: ('unknown_0xc6f86bfd', _decode_unknown_0xc6f86bfd),
    0xbfffe95a: ('unknown_0xbfffe95a', _decode_unknown_0xbfffe95a),
}
