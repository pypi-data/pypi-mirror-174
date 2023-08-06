import pytest
import torch
from typing import List
from aquatic.functional.stochastic_rounding import (
    stochastic_quantize,
)


@pytest.mark.parametrize("scale", [0.01, 0.1, 1.0])
@pytest.mark.parametrize("zero_point", [0, 10, 55, 32])
@pytest.mark.parametrize(
    "data", [torch.tensor([1.0]), torch.tensor([2.0, 5.0, -1.0]), torch.tensor([-1.0])]
)
def test_scale_exactly_divisible(data: torch.Tensor, scale: float, zero_point: int):
    int_output, fq_output = stochastic_quantize(
        data, scale=scale, zero_point=zero_point
    )
    assert (int_output == zero_point + data / scale).all()
    assert (fq_output == data).all()


@pytest.mark.parametrize("scale", [1.0, 0.1, 0.01])
@pytest.mark.parametrize("zero_point", [0, 10, 20])
def test_zero_point(zero_point: int, scale: float):
    data = torch.tensor([0.01, 0.0, 4])
    # Zero point is zero
    int_output, fq_output = stochastic_quantize(
        data, scale=scale, zero_point=zero_point
    )
    assert int_output[1] == zero_point  # Zero point should be as specified
    assert (
        fq_output[1] == 0
    )  # Zero point should have no effect on the actual zero value of the fake quantized value


def test_stochasticity(scale=1.0, zero_point=0):
    data = torch.ones(1000) * 0.5
    int_output, fq_output = stochastic_quantize(
        data, scale=scale, zero_point=zero_point
    )
    assert 1 in fq_output
    assert 0 in fq_output
    assert 1 in int_output
    assert 0 in int_output
    # This might be a risky test as this assumes that the stochastically speaking, the outcome will be within the specified hardcoded interval
    assert int_output.sum() > 0.45 * 1000
    assert int_output.sum() < 0.55 * 1000
