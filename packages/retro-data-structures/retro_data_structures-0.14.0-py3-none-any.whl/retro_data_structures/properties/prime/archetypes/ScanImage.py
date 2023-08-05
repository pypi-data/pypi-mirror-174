# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.core.AssetId import AssetId


@dataclasses.dataclass()
class ScanImage(BaseProperty):
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=0xffffffff)
    appear_percentage: float = dataclasses.field(default=0.0)
    unnamed: enums.ScanImagePane = dataclasses.field(default=enums.ScanImagePane._None)
    animation_cell_width: int = dataclasses.field(default=0)
    animation_cell_height: int = dataclasses.field(default=0)
    animation_swap_interval: float = dataclasses.field(default=0.0)
    fade_time: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        texture = struct.unpack(">L", data.read(4))[0]
        appear_percentage = struct.unpack('>f', data.read(4))[0]
        unnamed = enums.ScanImagePane.from_stream(data)
        animation_cell_width = struct.unpack('>l', data.read(4))[0]
        animation_cell_height = struct.unpack('>l', data.read(4))[0]
        animation_swap_interval = struct.unpack('>f', data.read(4))[0]
        fade_time = struct.unpack('>f', data.read(4))[0]
        return cls(texture, appear_percentage, unnamed, animation_cell_width, animation_cell_height, animation_swap_interval, fade_time)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack(">L", self.texture))
        data.write(struct.pack('>f', self.appear_percentage))
        self.unnamed.to_stream(data)
        data.write(struct.pack('>l', self.animation_cell_width))
        data.write(struct.pack('>l', self.animation_cell_height))
        data.write(struct.pack('>f', self.animation_swap_interval))
        data.write(struct.pack('>f', self.fade_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            texture=data['texture'],
            appear_percentage=data['appear_percentage'],
            unnamed=enums.ScanImagePane.from_json(data['unnamed']),
            animation_cell_width=data['animation_cell_width'],
            animation_cell_height=data['animation_cell_height'],
            animation_swap_interval=data['animation_swap_interval'],
            fade_time=data['fade_time'],
        )

    def to_json(self) -> dict:
        return {
            'texture': self.texture,
            'appear_percentage': self.appear_percentage,
            'unnamed': self.unnamed.to_json(),
            'animation_cell_width': self.animation_cell_width,
            'animation_cell_height': self.animation_cell_height,
            'animation_swap_interval': self.animation_swap_interval,
            'fade_time': self.fade_time,
        }
