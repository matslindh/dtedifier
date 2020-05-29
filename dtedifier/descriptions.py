import struct

from dataclasses import dataclass
from .exceptions import (
    InvalidBlockIdentifier,
)

from .utils import (
    degrees_string_to_float,
    na_or_int,
    four_digit_single_decimal,
    empty_or_int,
    convert_signed_16bfixed,
)


def structure_mapping_parser(data_mapping, b):
    arguments = {}

    for field, location in data_mapping.items():
        data = b[location[0] - 1:location[1]]

        if len(location) > 2:
            for f in location[2:]:
                if f == str:
                    data = data.decode('utf-8')
                else:
                    data = f(data)

        arguments[field] = data

    return arguments


@dataclass
class Header:
    longitude: float
    latitude: float
    longitude_interval: float
    latitude_interval: float
    absolute_vertical_accuracy: int
    unclassified_security_code: str
    unique_reference_number: str
    number_of_longitude_lines: int
    number_of_latitude_points: int
    multiple_accuracy: bool
    reserved: bytes

    # These are directly from standard documents, so they're 1-based (and the last bytes is inclusive)
    data_mapping = {
        'longitude': [5, 12, str, degrees_string_to_float],
        'latitude': [13, 20, str, degrees_string_to_float],
        'longitude_interval': [21, 24, str, four_digit_single_decimal],
        'latitude_interval': [25, 28, str, four_digit_single_decimal],
        'absolute_vertical_accuracy': [29, 32, str, na_or_int],
        'unclassified_security_code': [33, 35, str],
        'unique_reference_number': [36, 47, str],
        'number_of_longitude_lines': [48, 51, int],
        'number_of_latitude_points': [52, 55, int],
        'multiple_accuracy': [56, 56, int, bool],
        'reserved': [57, 80]
    }

    @classmethod
    def from_bytes(cls, b):
        if b[0:4] != b'UHL1':
            raise InvalidBlockIdentifier('Expected UHL1 as user header block prefix')

        return cls(**structure_mapping_parser(cls.data_mapping, b))


@dataclass
class DataSetDescription:
    security_control_and_release: str
    security_handling_description: str
    dma_series_designator: str

    unique_reference_number: str
    data_edition_number: str
    match_merge_version: str
    maintenance_date: str
    match_merge_date: str
    maintenance_description_code: str

    producer_code: str
    product_specification: str
    product_specification_numeric: int
    product_specification_date: str
    vertical_datum: str
    horizontal_datum: str
    collection_system: str
    compilation_date: str

    latitude_of_origin: float
    longitude_of_origin: float
    latitude_of_sw_corner: float
    longitude_of_sw_corner: float
    latitude_of_nw_corner: float
    longitude_of_nw_corner: float
    latitude_of_ne_corner: float
    longitude_of_ne_corner: float
    latitude_of_se_corner: float
    longitude_of_se_corner: float

    orientation_angle: float
    latitude_interval: float
    longitude_interval: float

    number_of_latitude_lines: int
    number_of_longitude_lines: int

    partial_cell: int
    coverage_in_percent: int
    geoid_undulation: str

    # These are directly from standard documents, so they're 1-based (and the last bytes is inclusive)
    data_mapping = {
        'security_control_and_release': [5, 6, str],
        'security_handling_description': [7, 33, str],
        'dma_series_designator': [60, 64, str],

        'unique_reference_number': [65, 79, str],
        'data_edition_number': [88, 89, int],
        'match_merge_version': [90, 90, str],
        'maintenance_date': [91, 94, str],
        'match_merge_date': [95, 98, str],
        'maintenance_description_code': [99, 102, int],

        'producer_code': [103, 100, str],
        'product_specification': [127, 135, str],
        'product_specification_numeric': [136, 137, int],
        'product_specification_date': [138, 141, str],
        'vertical_datum': [142, 144, str],
        'horizontal_datum': [145, 149, str],
        'collection_system': [150, 159, str],
        'compilation_date': [160, 163, str],

        'latitude_of_origin': [186, 194, str, degrees_string_to_float],
        'longitude_of_origin': [195, 204, str, degrees_string_to_float],
        'latitude_of_sw_corner': [205, 211, str, degrees_string_to_float],
        'longitude_of_sw_corner': [212, 219, str, degrees_string_to_float],
        'latitude_of_nw_corner': [220, 226, str, degrees_string_to_float],
        'longitude_of_nw_corner': [227, 234, str, degrees_string_to_float],
        'latitude_of_ne_corner': [235, 241, str, degrees_string_to_float],
        'longitude_of_ne_corner': [242, 249, str, degrees_string_to_float],
        'latitude_of_se_corner': [250, 256, str, degrees_string_to_float],
        'longitude_of_se_corner': [257, 264, str, degrees_string_to_float],

        'orientation_angle': [265, 273, float],
        'latitude_interval': [274, 277, str, four_digit_single_decimal],
        'longitude_interval': [278, 281, str, four_digit_single_decimal],
        'number_of_latitude_lines': [282, 285, int],
        'number_of_longitude_lines': [286, 289, int],

        'partial_cell': [290, 291, int],
        'coverage_in_percent': [292, 392, empty_or_int],
        'geoid_undulation': [393, 492, str],
    }

    @classmethod
    def from_bytes(cls, b):
        if b[0:3] != b'DSI':
            raise InvalidBlockIdentifier('Expected DSI as data set block prefix')

        return cls(**structure_mapping_parser(cls.data_mapping, b))


@dataclass
class AccuracyDescription:
    absolute_horizontal_accuracy: int
    absolute_vertical_accuracy: int
    relative_horizontal_accuracy: int
    relative_vertical_accuracy: int
    multiple_accuracy_outline_flag: str

    data_mapping = {
        'absolute_horizontal_accuracy': [4, 7, str, na_or_int],
        'absolute_vertical_accuracy': [8, 11, str, na_or_int],
        'relative_horizontal_accuracy': [12, 15, str, na_or_int],
        'relative_vertical_accuracy': [16, 19, str, na_or_int],
        'multiple_accuracy_outline_flag': [56, 57, str],
    }

    @classmethod
    def from_bytes(cls, b):
        if b[0:3] != b'ACC':
            raise InvalidBlockIdentifier('Expected ACC as accuracy block prefix')

        return cls(**structure_mapping_parser(cls.data_mapping, b))


@dataclass
class DataRecord:
    elevation: list

    def elevation_north_south(self):
        return list(reversed(self.elevation))

    def elevation_trimmed(self):
        elevation = self.elevation_north_south()
        first_row_with_data = None
        last_row_with_data = -1
        first_column_with_data = None
        last_column_with_data = -1

        for idx, row in enumerate(elevation):
            has_data = any(row)

            if has_data:
                if not first_row_with_data:
                    first_row_with_data = idx

                if idx > last_row_with_data:
                    last_row_with_data = idx

                first_column = next(idx for idx, val in enumerate(row) if val is not None)
                last_column = len(row) - next(idx for idx, val in enumerate(reversed(row)) if val is not None) - 1

                if first_column_with_data is None or first_column < first_column_with_data:
                    first_column_with_data = first_column

                last_column_with_data = max(last_column_with_data, last_column)

        keep = []

        for row in elevation[first_row_with_data:last_row_with_data + 1]:
            keep.append(row[first_column_with_data:last_column_with_data+1])

        return keep

    @classmethod
    def from_bytes(cls, b, data_set_description):
        block_metadata_len = 12
        bytes_per_data_point = 2

        block_size = block_metadata_len + data_set_description.number_of_latitude_lines * bytes_per_data_point
        elevation = []

        for i in range(0, data_set_description.number_of_longitude_lines):
            offset = i*block_size
            block = b[offset:offset+block_size]

            if block[0] != 170:
                raise InvalidBlockIdentifier('Expected first byte to have the value 170 when reading data record.')

            longitude_index = struct.unpack('>H', block[4:6])[0]
            latitude_index = struct.unpack('>H', block[6:8])[0]

            elevation_line = struct.unpack('>' + str(data_set_description.number_of_latitude_lines) + 'h', block[8:-4])
            elevation.append(map(convert_signed_16bfixed, elevation_line))
            checksum = struct.unpack('>I', b[-4:])

        # the data set is longitude based - so it needs to be rotated to be oriented correctly
        elevation = list(map(list, zip(*elevation)))

        return DataRecord(elevation=elevation)


