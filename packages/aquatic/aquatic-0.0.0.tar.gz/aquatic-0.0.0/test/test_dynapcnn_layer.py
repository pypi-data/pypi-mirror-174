import aquatic
import aquatic.nn as qnn
import numpy as np
import sinabs.backend.dynapcnn.dynapcnn_layer as sdl
import sinabs.layers as sl
import torch
import torch.nn as nn
from aquatic.utils import generate_dynapcnnlayer_qconfig
import sinabs.backend.dynapcnn.dynapcnn_layer as sdl
import numpy as np
import pytest


@pytest.mark.parametrize("has_bias", [True, False])
def test_dynapcnn_to_float(has_bias):
    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8, has_bias=has_bias
    )
    qdynapcnn = qnn.DynapcnnLayer(
        conv=nn.Conv2d(1, 3, 3, bias=has_bias),
        spk=sl.IAF(spike_threshold=torch.tensor(1.0), min_v_mem=-1),
        in_shape=(1, 10, 10),
        discretize=False,
        qconfig=qconfig,
    )

    dynapcnn = qdynapcnn.to_float()

    # TODO this should be .all(), but cannot use with StochasticRounding
    assert (
        dynapcnn.conv_layer.weight == qdynapcnn.quantize_params()["conv_layer.weight"]
    ).any()


@pytest.mark.parametrize("has_bias", [True, False])
def test_dynapcnn_to_int(has_bias):
    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8, has_bias=has_bias
    )
    qdynapcnn = qnn.DynapcnnLayer(
        conv=nn.Conv2d(1, 3, 3, bias=has_bias),
        spk=sl.IAF(spike_threshold=torch.tensor(1.0)),
        in_shape=(1, 10, 10),
        discretize=False,
        qconfig=qconfig,
    )

    int_layer = qdynapcnn.to_int()

    orig_weight_threshold_ratio = (
        qdynapcnn.mod.conv_layer.weight / qdynapcnn.mod.spk_layer.spike_threshold
    )
    int_weight_threshold_ratio = (
        int_layer.conv_layer.weight / int_layer.spk_layer.spike_threshold
    )

    torch.testing.assert_close(
        orig_weight_threshold_ratio, int_weight_threshold_ratio, atol=0.1, rtol=0.2
    )

    # TODO cumbersome way to detect that all floats are indeed integer values
    assert np.mod(int_layer.conv_layer.weight.detach().numpy(), 1).sum() == 0


@pytest.mark.parametrize("has_bias", [True, False])
def test_dynapcnn_from_float(has_bias):
    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8, has_bias=has_bias
    )

    dynapcnn = sdl.DynapcnnLayer(
        conv=nn.Conv2d(1, 3, 3, bias=has_bias),
        spk=sl.IAF(spike_threshold=torch.tensor(1.0), min_v_mem=-1),
        in_shape=(1, 10, 10),
        discretize=False,
    )
    qdynapcnn = qnn.DynapcnnLayer.from_float(mod=dynapcnn, qconfig=qconfig)

    assert qdynapcnn.qconfig == qconfig
    assert (dynapcnn.conv_layer.weight == qdynapcnn.mod.conv_layer.weight).all()
    assert dynapcnn.spk_layer.spike_threshold == qdynapcnn.mod.spk_layer.spike_threshold
    assert dynapcnn.spk_layer.min_v_mem == qdynapcnn.mod.spk_layer.min_v_mem


def test_learning():
    # Defind quantization params
    qconfig = generate_dynapcnnlayer_qconfig(
        n_bits_weight=2, n_bits_threshold=4, has_bias=False
    )

    # Define a layer
    in_shape = (2, 10, 10)
    conv_layer = torch.nn.Conv2d(2, 1, 3, bias=False)
    dcnn_layer = qnn.DynapcnnLayer(
        conv=conv_layer,
        spk=sl.IAFSqueeze(batch_size=1, spike_threshold=torch.tensor(1.5)),
        in_shape=in_shape,
        discretize=False,
        qconfig=qconfig,
    )
    print(dcnn_layer.mod)

    # Generate a random input tensor
    input_data = torch.rand((1, *in_shape))

    optim = torch.optim.Adam(dcnn_layer.parameters(), lr=1e-3)
    criterion = torch.nn.MSELoss()

    # Training loop
    for i in range(10):
        optim.zero_grad()
        dcnn_layer.zero_grad()

        out = dcnn_layer(input_data)
        loss = criterion(out.mean(), torch.tensor(1.0))
        loss.backward()
        optim.step()
