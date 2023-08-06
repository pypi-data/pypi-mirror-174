import torch
from aquatic.calculate_qparam import calculate_qparams_lif
from aquatic.nn.dynapcnn_layer import DynapcnnLayer
from aquatic.observer import SharedObserver, SharedObserverContainer
from aquatic.qconfig import QConfig
from aquatic.fake_quantize import FakeQuantize
from aquatic.quantizer import NoZeroShiftUniformStochasticRounding
import sinabs.layers as sl
import sinabs


def test_shared_observer_instantiation():
    container = SharedObserverContainer()

    weight_observer = SharedObserver.with_args(var_name="weight", container=container)()
    threshold_observer = SharedObserver.with_args(
        var_name="spike_threshold", container=container
    )()

    weight_rand = torch.rand(20)
    threshold = torch.tensor(1.0)

    weight_observer(weight_rand)
    threshold_observer(threshold)

    assert "weight" in container.states
    assert "spike_threshold" in container.states

    # print(weight_observer)


def test_qconfig_shared():
    container = SharedObserverContainer()
    weight_bitwidth = 8
    spike_threshold_bitwidth = 8
    qconfig = QConfig(
        weight=FakeQuantize.with_args(
            observer=SharedObserver.with_args(var_name="weight", container=container),
            quantizer=NoZeroShiftUniformStochasticRounding(
                quant_max=2 ** (weight_bitwidth - 1) - 1,
                quant_min=-(2 ** (weight_bitwidth - 1)),
            ),
            qparam_calculator=lambda x, y: (1, 0),
        ),
        spike_threshold=FakeQuantize.with_args(
            observer=SharedObserver.with_args(
                var_name="spike_threshold", container=container
            ),
            quantizer=NoZeroShiftUniformStochasticRounding(
                quant_max=2**spike_threshold_bitwidth - 1,
                quant_min=-(2**spike_threshold_bitwidth),
            ),
            qparam_calculator=lambda x, y: (1, 0),
        ),
    )

    dcnn_layer = DynapcnnLayer(
        conv=torch.nn.Conv2d(1, 1, 3, bias=False),
        spk=sl.IAFSqueeze(
            spike_fn=sinabs.activation.MultiSpike,
            batch_size=1,
            spike_threshold=torch.tensor(1.5),
        ),
        in_shape=(2, 10, 10),
        discretize=False,
        qconfig=qconfig,
    )

    quantized_params = dcnn_layer.quantize_params()

    assert "weight" in container.observer_handles
    assert "spike_threshold" in container.observer_handles
