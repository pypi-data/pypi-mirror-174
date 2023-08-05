# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId


@dataclasses.dataclass()
class ScanTreeSlider(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    name_string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=0xffffffff)
    name_string_name: str = dataclasses.field(default='')
    unknown: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'SCSL'

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F!\x9b\xac')  # 0x46219bac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.name_string_table))

        data.write(b'2i\x8b\xd6')  # 0x32698bd6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.name_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02a\xa4\xe0')  # 0x261a4e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            name_string_table=data['name_string_table'],
            name_string_name=data['name_string_name'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'name_string_table': self.name_string_table,
            'name_string_name': self.name_string_name,
            'unknown': self.unknown,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_name_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_name_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x46219bac: ('name_string_table', _decode_name_string_table),
    0x32698bd6: ('name_string_name', _decode_name_string_name),
    0x261a4e0: ('unknown', _decode_unknown),
}
