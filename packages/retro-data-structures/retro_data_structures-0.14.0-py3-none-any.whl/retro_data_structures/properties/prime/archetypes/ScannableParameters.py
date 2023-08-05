# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.AssetId import AssetId


@dataclasses.dataclass()
class ScannableParameters(BaseProperty):
    scan_file: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=0xffffffff)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        scan_file = struct.unpack(">L", data.read(4))[0]
        return cls(scan_file)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack(">L", self.scan_file))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_file=data['scan_file'],
        )

    def to_json(self) -> dict:
        return {
            'scan_file': self.scan_file,
        }
