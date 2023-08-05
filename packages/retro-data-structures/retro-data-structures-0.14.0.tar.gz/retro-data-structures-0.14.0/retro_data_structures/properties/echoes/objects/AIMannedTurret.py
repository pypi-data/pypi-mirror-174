# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.UnknownStruct3 import UnknownStruct3
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class AIMannedTurret(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct3: UnknownStruct3 = dataclasses.field(default_factory=UnknownStruct3)
    patrol_horiz_spline: Spline = dataclasses.field(default_factory=Spline)
    patrol_vertical_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def object_type(cls) -> str:
        return 'AIMT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['AIMannedTurret.rel']

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
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1]\xeco')  # 0xb15dec6f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\x07\x92\xcf')  # 0x260792cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol_horiz_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84(K\x1c')  # 0x84284b1c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol_vertical_spline.to_stream(data)
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
            unknown_struct3=UnknownStruct3.from_json(data['unknown_struct3']),
            patrol_horiz_spline=Spline.from_json(data['patrol_horiz_spline']),
            patrol_vertical_spline=Spline.from_json(data['patrol_vertical_spline']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct3': self.unknown_struct3.to_json(),
            'patrol_horiz_spline': self.patrol_horiz_spline.to_json(),
            'patrol_vertical_spline': self.patrol_vertical_spline.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_unknown_struct3(data: typing.BinaryIO, property_size: int):
    return UnknownStruct3.from_stream(data, property_size)


def _decode_patrol_horiz_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_patrol_vertical_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb15dec6f: ('unknown_struct3', _decode_unknown_struct3),
    0x260792cf: ('patrol_horiz_spline', _decode_patrol_horiz_spline),
    0x84284b1c: ('patrol_vertical_spline', _decode_patrol_vertical_spline),
}
