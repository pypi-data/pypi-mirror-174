import torch
import sinabs.layers as sl
from aquatic.nn.lif import LIF
from aquatic import QConfig
import pytest


def test_passthrough():
    layer = LIF(tau_mem=10.0, qconfig=QConfig())

    data = torch.rand((10, 100))

    out = layer(data)
    # print(out)


@pytest.mark.parametrize(
    "tau_mem_orig, quant_max, tau_mem_quantized",
    [(20.0, 10, 10.0), (15.5, 10, 10.0), (0.0, 10, 0), (8.0, 10, 8.0)],
)
def test_tau_quantization(
    tau_mem_orig: float, quant_max: int, tau_mem_quantized: float
):
    from aquatic.quantizer import FixedQParamsUniformStochasticRounding

    qconfig = QConfig(
        tau=FixedQParamsUniformStochasticRounding.with_args(
            quant_min=-10, quant_max=quant_max, zero_point=0, scale=1.0
        )
    )
    layer = LIF(tau_mem=tau_mem_orig, qconfig=qconfig)

    quantized_params = layer.quantize_params()
    assert quantized_params["tau_mem"] == tau_mem_quantized


@pytest.mark.parametrize(
    "tau_orig, quant_max, tau_quantized",
    [(20.0, 10, 10.0), (15.5, 10, 10.0), (0.0, 10, 0.0), (8.0, 10, 8.0)],
)
def test_tau_syn_quantization(tau_orig: float, quant_max: int, tau_quantized: float):
    from aquatic.quantizer import FixedQParamsUniformStochasticRounding

    qconfig = QConfig(
        tau=FixedQParamsUniformStochasticRounding.with_args(
            quant_min=-10, quant_max=quant_max, zero_point=0, scale=1.0
        )
    )
    layer = LIF(tau_mem=tau_orig, tau_syn=tau_orig, qconfig=qconfig)

    quantized_params = layer.quantize_params()
    assert quantized_params["tau_mem"] == tau_quantized
    assert quantized_params["tau_syn"] == tau_quantized
