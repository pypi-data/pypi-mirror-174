# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId


@dataclasses.dataclass()
class UnknownStruct173(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    title_strings: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    instruction: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    instruction_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    music_names: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffffffffffff)
    text_background: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=0xffffffffffffffff)

    @classmethod
    def game(cls) -> Game:
        return Game.DKCRETURNS

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xc8G\xc0')  # 0x17c847c0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_strings))

        data.write(b'7\xfd\x19\x13')  # 0x37fd1913
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.instruction))

        data.write(b'\xa1O4\xca')  # 0xa14f34ca
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.instruction_core))

        data.write(b'\x1b\xd68Y')  # 0x1bd63859
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.music_names))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            title_strings=data['title_strings'],
            instruction=data['instruction'],
            instruction_core=data['instruction_core'],
            music_names=data['music_names'],
            back=data['back'],
            back_core=data['back_core'],
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title_strings': self.title_strings,
            'instruction': self.instruction,
            'instruction_core': self.instruction_core,
            'music_names': self.music_names,
            'back': self.back,
            'back_core': self.back_core,
            'text_background': self.text_background,
        }


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_title_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_instruction(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_instruction_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_music_names(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', _decode_unknown_struct29),
    0x17c847c0: ('title_strings', _decode_title_strings),
    0x37fd1913: ('instruction', _decode_instruction),
    0xa14f34ca: ('instruction_core', _decode_instruction_core),
    0x1bd63859: ('music_names', _decode_music_names),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xe119319b: ('text_background', _decode_text_background),
}
