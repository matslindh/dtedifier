from dtedifier.descriptions import (
    Header,
    DataSetDescription,
    AccuracyDescription,
)

from pytest import (
    approx,
    fixture,
)


@fixture
def example_header():
    return Header.from_bytes(b'UHL10100000E0590000N00200010NA  U              180136010                        ')


@fixture
def example_data_set():
    return DataSetDescription.from_bytes(b'DSIU                                                       DTED2000000000000000        01A000000000000                        PRF89020B000005MSLWGS84                                    590000.0N0100000.0E590000N0100000E600000N0100000E600000N0110000E590000N0110000E0000000.0001000203601180101                                                                                                                                                                                                                                                                                                                                                                     ')


@fixture
def example_accuracy_description():
    return AccuracyDescription.from_bytes(b'ACCNA  NA  NA  NA                                      00                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ')


def test_header_parser(example_header):
    assert example_header.longitude == approx(10.0)
    assert example_header.latitude == approx(59.0)
    assert example_header.longitude_interval == 2.0
    assert example_header.latitude_interval == 1.0
    assert example_header.absolute_vertical_accuracy is None
    assert not example_header.multiple_accuracy
    assert example_header.number_of_longitude_lines == 1801
    assert example_header.number_of_latitude_points == 3601


def test_data_set_parser(example_data_set):
    pass


def test_accuracy_description_parser(example_accuracy_description):
    pass