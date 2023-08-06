import sinabs
import sinabs.layers as sl
import torch
from aquatic.calculate_qparam import calculate_qparams_lif
from aquatic.fake_quantize import FakeQuantize
from aquatic.nn.dynapcnn_layer import DynapcnnLayer
from aquatic.observer import SharedObserver, SharedObserverContainer
from aquatic.qconfig import QConfig
from aquatic.quantizer import (
    NoZeroShiftUniformStochasticRounding,
    SharedQuantizer,
    SharedQuantizerContainer,
    FixedQParamsUniformStochasticRounding,
)


def test_sharing():
    container = SharedQuantizerContainer()

    weight_quantizer = SharedQuantizer(
        quantizer=NoZeroShiftUniformStochasticRounding(quant_min=-8, quant_max=7),
        container=container,
        var_name="weight",
    )
    threshold_quantizer = SharedQuantizer(
        quantizer=NoZeroShiftUniformStochasticRounding(quant_min=-64, quant_max=63),
        container=container,
        var_name="spike_threshold",
    )

    assert "weight" in container.quantizer_handles
    assert "spike_threshold" in container.quantizer_handles


def test_calculate_qparams_lif():
    quantizer_container = SharedQuantizerContainer()
    observer_container = SharedObserverContainer()

    qconfig = QConfig(
        weight=FakeQuantize.with_args(
            observer=SharedObserver.with_args(
                var_name="weight", container=observer_container
            ),
            quantizer=SharedQuantizer(
                quantizer=NoZeroShiftUniformStochasticRounding(
                    quant_min=-128, quant_max=127
                ),
                container=quantizer_container,
                var_name="weight",
            ),
            qparam_calculator=calculate_qparams_lif,
        ),
        bias=FakeQuantize.with_args(
            observer=SharedObserver.with_args(
                var_name="bias", container=observer_container
            ),
            quantizer=SharedQuantizer(
                quantizer=NoZeroShiftUniformStochasticRounding(
                    quant_min=-128, quant_max=127
                ),
                container=quantizer_container,
                var_name="bias",
            ),
            qparam_calculator=calculate_qparams_lif,
        ),
        spike_threshold=FakeQuantize.with_args(
            observer=SharedObserver.with_args(
                var_name="spike_threshold", container=observer_container
            ),
            quantizer=SharedQuantizer(
                quantizer=NoZeroShiftUniformStochasticRounding(
                    quant_min=0, quant_max=255
                ),
                container=quantizer_container,
                var_name="spike_threshold",
            ),
            qparam_calculator=calculate_qparams_lif,
        ),
    )

    conv_layer = torch.nn.Conv2d(1, 1, 3)
    # conv_layer.weight.data = torch.rand((3,3))

    dcnn_layer = DynapcnnLayer(
        conv=conv_layer,
        spk=sl.IAFSqueeze(batch_size=1, spike_threshold=torch.tensor(1.5)),
        in_shape=(2, 10, 10),
        discretize=False,
        qconfig=qconfig,
    )

    # print(dcnn_layer.mod.spk_layer.spike_threshold)

    quantized_params = dcnn_layer.quantize_params()
    # print(quantized_params)

    # print(dcnn_layer.weight_quantize.calculate_qparams())
    # print(dcnn_layer.bias_quantize.calculate_qparams())
    # print(dcnn_layer.spike_threshold_quantize.calculate_qparams())

    int_module = dcnn_layer.to_int()
    # print(int_module.conv_layer.weight)
    # print(int_module.conv_layer.bias)
    # print(int_module.spk_layer.spike_threshold)


def test_quantize_thresholds():
    qconfig = QConfig(
        spike_threshold=FixedQParamsUniformStochasticRounding.with_args(
            quant_min=0, quant_max=255
        ),
    )

    dcnn_layer = DynapcnnLayer(
        conv=torch.nn.Conv2d(1, 1, 3),
        spk=sl.IAFSqueeze(batch_size=1, spike_threshold=torch.tensor(1.5)),
        in_shape=(2, 10, 10),
        discretize=False,
        qconfig=qconfig,
    )

    quantized_params = dcnn_layer.quantize_params()

    # print(quantized_params)
