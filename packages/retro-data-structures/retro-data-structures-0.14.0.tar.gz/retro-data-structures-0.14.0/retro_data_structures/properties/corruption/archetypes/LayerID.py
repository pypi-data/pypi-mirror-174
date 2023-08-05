# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.corruption.core.AssetId import AssetId


@dataclasses.dataclass()
class LayerID(BaseProperty):
    area_id: AssetId = dataclasses.field(metadata={'asset_types': []}, default=0xffffffffffffffff)
    layer_id: SavedStateID = dataclasses.field(default_factory=SavedStateID)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        area_id = struct.unpack(">Q", data.read(8))[0]
        layer_id = SavedStateID.from_stream(data, property_size)
        return cls(area_id, layer_id)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack(">Q", self.area_id))
        self.layer_id.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            area_id=data['area_id'],
            layer_id=SavedStateID.from_json(data['layer_id']),
        )

    def to_json(self) -> dict:
        return {
            'area_id': self.area_id,
            'layer_id': self.layer_id.to_json(),
        }
