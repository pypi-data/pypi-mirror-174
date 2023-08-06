import pytest
from typing import Any
from aquatic.calculate_qparam import (
    calculate_uniform_qparam_from_range,
    calculate_uniform_qparam_from_range_no_zero_shift,
)


@pytest.mark.parametrize("scale_orig", [1, 0.5, 0.001])
@pytest.mark.parametrize("zero_point_orig", [0, 3, 10])
def test_ternary(scale_orig: float, zero_point_orig: int):
    scale, zero_point = calculate_uniform_qparam_from_range(
        -1 * scale_orig, 1 * scale_orig, -1 + zero_point_orig, 1 + zero_point_orig
    )
    assert scale == scale_orig
    assert zero_point == zero_point_orig


def test_8bit_quant():
    scale, zero_point = calculate_uniform_qparam_from_range(-128, 127, -128, 127)
    assert scale == 1
    assert zero_point == 0


@pytest.mark.parametrize(
    "min_value, max_value, scale_orig", [(-128, 127, 1), (-128, 0, 1), (-1, 127, 1)]
)
def test_8bit_no_zero_point(min_value, max_value, scale_orig):
    scale, zero_point = calculate_uniform_qparam_from_range_no_zero_shift(
        min_value, max_value, -128, 127
    )
    assert scale == scale_orig
    assert zero_point == 0
