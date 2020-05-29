from dtedifier.utils import (
    degrees_string_to_float,
    na_or_int,
    empty_or_int,
    convert_signed_16bfixed,
)

from pytest import (
    approx
)


def test_degrees_string_to_float():
    assert degrees_string_to_float('1001010E') == approx(100.16944444)
    assert degrees_string_to_float('0505959E') == approx(50.99972222)
    assert degrees_string_to_float('1001010W') == approx(-100.16944444)
    assert degrees_string_to_float('0505959W') == approx(-50.99972222)

    assert degrees_string_to_float('0505959N') == approx(50.99972222)
    assert degrees_string_to_float('0505959S') == approx(-50.99972222)

    assert degrees_string_to_float('424242.42') == approx(42.71178333)


def test_na_or_int():
    assert na_or_int('NA  ') is None
    assert na_or_int('341') == 341
    assert na_or_int('341     ') == 341


def test_empty_or_int():
    assert empty_or_int('   ') is None
    assert empty_or_int('1231   ') == 1231


def test_convert_signed_16bfixed():
    assert convert_signed_16bfixed(-1) is None
    assert convert_signed_16bfixed(-2) == -32766
    assert convert_signed_16bfixed(2) == 2
    assert convert_signed_16bfixed(32767) == 32767
