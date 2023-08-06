import pytest
import torch
from typing import List
from aquatic.quantizer import (
    FixedQParamsUniformStochasticRounding,
    TauStochasticRoundingToBitShift,
    AlphaStochsticRoundingToBitShift,
)


@pytest.mark.parametrize(
    "scale, expected", [(1.0, [0, 1]), (0.1, [0.5]), (0.01, [0.5])]
)
def test_fixed_params_sr(scale: float, expected: List):
    data = torch.tensor([0.5])
    # Define quantizer with default parameters
    FSR = FixedQParamsUniformStochasticRounding.with_args(scale=scale)
    my_quantizer = FSR()

    assert my_quantizer.scale == scale
    assert my_quantizer.zero_point == 0.0

    for i in range(100):
        assert my_quantizer(data) in expected


@pytest.mark.parametrize("tau", torch.arange(1, 32))
def test_tau_bitshift_sr(tau: float):
    TauSR = TauStochasticRoundingToBitShift.with_args(quant_max=3)
    tau_quantizer = TauSR()
    assert tau_quantizer.quant_max == 3

    tau_quantized = tau_quantizer(tau)
    # The maximum value allowed by 3 bit shifts is 8
    assert tau_quantized <= 8
    if tau <= 2:
        assert tau_quantized in [1, 2]
    elif tau <= 4:
        assert tau_quantized in [2, 4]
    elif tau <= 8:
        assert tau_quantized in [4, 8]
    else:
        assert tau_quantized == 8


@pytest.mark.parametrize("alpha", torch.arange(0.4, 0.9999, 0.01))
def test_alpha_bitshift_sr(alpha: float):
    AlphaSR = AlphaStochsticRoundingToBitShift.with_args(quant_max=3)
    alpha_quantizer = AlphaSR()

    alpha_quantized = alpha_quantizer(alpha)

    if alpha <= 0.5:
        assert alpha_quantized in [0, 0.5]
    elif alpha <= 0.75:
        assert alpha_quantized in [0.5, 0.75]
    else:
        alpha == 0.75
