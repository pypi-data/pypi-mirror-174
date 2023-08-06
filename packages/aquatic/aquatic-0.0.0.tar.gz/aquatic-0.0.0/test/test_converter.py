from audioop import add
from copy import deepcopy
import aquatic.nn as qnn
import torch.nn as nn
import torch
import aquatic
import sinabs
import sinabs.layers as sl
import sinabs.backend.dynapcnn.dynapcnn_layer as sdl


class CNN(nn.Sequential):
    def __init__(self):
        super().__init__(
            nn.Conv2d(2, 20, 5, 1, bias=False),
            nn.ReLU(),
            sl.SumPool2d(2, 2),
            nn.Conv2d(20, 32, 5, 1, bias=False),
            nn.ReLU(),
            sl.SumPool2d(2, 2),
            nn.Conv2d(32, 128, 3, 1, bias=False),
            nn.ReLU(),
            sl.SumPool2d(2, 2),
            nn.Flatten(),
            nn.Linear(128, 500, bias=False),
            nn.ReLU(),
            nn.Linear(500, 10, bias=False),
        )


def test_convert_torch_model_to_qat_model():
    model = CNN()
    qconfig = aquatic.QConfig()
    q_model = aquatic.prepare_qat(model, qconfig=qconfig)

    assert len(q_model) == len(model)
    assert isinstance(q_model[0], qnn.Conv2d)
    assert isinstance(q_model[1], nn.ReLU)
    assert isinstance(q_model[3], qnn.Conv2d)
    assert isinstance(q_model[4], nn.ReLU)
    assert isinstance(q_model[10], qnn.Linear)


def test_convert_torch_model_to_qat_model():
    model = CNN()
    snn = sinabs.from_model(model, batch_size=1, add_spiking_output=True).spiking_model

    input_shape = (1, 28, 28)
    dynapcnn_model = sinabs.backend.dynapcnn.DynapcnnNetwork(
        snn,
        input_shape=input_shape,
        dvs_input=False,
        discretize=False,
    )

    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8
    )
    q_model = aquatic.prepare_qat(dynapcnn_model, qconfig=qconfig)

    assert isinstance(q_model.sequence[0], qnn.DynapcnnLayer)
    assert isinstance(q_model.sequence[1], qnn.DynapcnnLayer)
    assert isinstance(q_model.sequence[2], qnn.DynapcnnLayer)
    assert isinstance(q_model.sequence[3], qnn.DynapcnnLayer)
    assert isinstance(q_model.sequence[4], qnn.DynapcnnLayer)
    assert q_model.sequence[0].qconfig is not q_model.sequence[1].qconfig


def test_convert_qat_model_to_torch_model():
    qconfig = aquatic.QConfig()
    qmodel = nn.Sequential(
        qnn.Conv2d(2, 8, 3, qconfig=qconfig),
        nn.ReLU(),
        qnn.Conv2d(8, 16, 3, qconfig=qconfig),
        nn.ReLU(),
        nn.Flatten(),
        qnn.Linear(100, 10, qconfig=qconfig),
    )

    model = aquatic.to_float_model(qmodel)

    assert len(qmodel) == len(model)
    assert isinstance(model[0], nn.Conv2d)
    assert isinstance(model[1], nn.ReLU)
    assert isinstance(model[2], nn.Conv2d)
    assert isinstance(model[3], nn.ReLU)
    assert isinstance(model[5], nn.Linear)


def test_convert_qat_dynapcnn_model_to_float():
    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8
    )
    qmodel = nn.Sequential(
        qnn.DynapcnnLayer(
            conv=nn.Conv2d(1, 1, 3),
            spk=sl.IAF(spike_threshold=torch.tensor(1.0)),
            discretize=False,
            in_shape=(1, 28, 28),
            qconfig=deepcopy(qconfig),
        ),
        qnn.DynapcnnLayer(
            conv=nn.Conv2d(1, 1, 3),
            spk=sl.IAF(spike_threshold=torch.tensor(1.0)),
            discretize=False,
            in_shape=(1, 28, 28),
            qconfig=deepcopy(qconfig),
        ),
    )

    model = aquatic.to_float_model(qmodel)

    assert isinstance(model[0], sdl.DynapcnnLayer)
    assert isinstance(model[1], sdl.DynapcnnLayer)
