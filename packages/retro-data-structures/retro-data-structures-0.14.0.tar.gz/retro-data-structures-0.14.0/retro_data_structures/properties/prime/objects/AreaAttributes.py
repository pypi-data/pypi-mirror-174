# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.AssetId import AssetId


@dataclasses.dataclass()
class AreaAttributes(BaseObjectType):
    unknown: int = dataclasses.field(default=0)
    show_skybox: bool = dataclasses.field(default=False)
    environmental_effect: int = dataclasses.field(default=0)  # Choice
    initial_environmental_effect_density: float = dataclasses.field(default=0.0)
    initial_thermal_heat_level: float = dataclasses.field(default=0.0)
    x_ray_fog_distance: float = dataclasses.field(default=0.0)
    initial_world_lighting_level: float = dataclasses.field(default=0.0)
    skybox_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=0xffffffff)
    phazon_type: int = dataclasses.field(default=0)  # Choice

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def object_type(cls) -> int:
        return 0x4E

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        unknown = struct.unpack('>l', data.read(4))[0]
        show_skybox = struct.unpack('>?', data.read(1))[0]
        environmental_effect = struct.unpack(">L", data.read(4))[0]
        initial_environmental_effect_density = struct.unpack('>f', data.read(4))[0]
        initial_thermal_heat_level = struct.unpack('>f', data.read(4))[0]
        x_ray_fog_distance = struct.unpack('>f', data.read(4))[0]
        initial_world_lighting_level = struct.unpack('>f', data.read(4))[0]
        skybox_model = struct.unpack(">L", data.read(4))[0]
        phazon_type = struct.unpack(">L", data.read(4))[0]
        return cls(unknown, show_skybox, environmental_effect, initial_environmental_effect_density, initial_thermal_heat_level, x_ray_fog_distance, initial_world_lighting_level, skybox_model, phazon_type)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\t')  # 9 properties
        data.write(struct.pack('>l', self.unknown))
        data.write(struct.pack('>?', self.show_skybox))
        data.write(struct.pack(">L", self.environmental_effect))
        data.write(struct.pack('>f', self.initial_environmental_effect_density))
        data.write(struct.pack('>f', self.initial_thermal_heat_level))
        data.write(struct.pack('>f', self.x_ray_fog_distance))
        data.write(struct.pack('>f', self.initial_world_lighting_level))
        data.write(struct.pack(">L", self.skybox_model))
        data.write(struct.pack(">L", self.phazon_type))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            show_skybox=data['show_skybox'],
            environmental_effect=data['environmental_effect'],
            initial_environmental_effect_density=data['initial_environmental_effect_density'],
            initial_thermal_heat_level=data['initial_thermal_heat_level'],
            x_ray_fog_distance=data['x_ray_fog_distance'],
            initial_world_lighting_level=data['initial_world_lighting_level'],
            skybox_model=data['skybox_model'],
            phazon_type=data['phazon_type'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'show_skybox': self.show_skybox,
            'environmental_effect': self.environmental_effect,
            'initial_environmental_effect_density': self.initial_environmental_effect_density,
            'initial_thermal_heat_level': self.initial_thermal_heat_level,
            'x_ray_fog_distance': self.x_ray_fog_distance,
            'initial_world_lighting_level': self.initial_world_lighting_level,
            'skybox_model': self.skybox_model,
            'phazon_type': self.phazon_type,
        }
