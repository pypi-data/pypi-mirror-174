from sinabs.backend.dynapcnn import DynapcnnNetwork
import torch.nn as nn
import torch
import sinabs
import sinabs.layers as sl
import aquatic


def test_dynapcnn_network():
    has_bias = True
    ann = nn.Sequential(
        nn.Conv2d(2, 8, 3, bias=has_bias),
        nn.ReLU(),
        nn.AvgPool2d(2),
        nn.Conv2d(8, 16, 3, bias=has_bias),
        nn.ReLU(),
        nn.AvgPool2d(2),
        nn.Conv2d(16, 2, 3, bias=has_bias),
    )

    input_shape = (2, 28, 28)
    batch_size = 1
    snn = sinabs.from_model(
        ann, input_shape=input_shape, batch_size=batch_size, add_spiking_output=True
    ).spiking_model

    dynapcnn_network = DynapcnnNetwork(
        snn=snn, input_shape=input_shape, discretize=True
    )

    num_timesteps = 100
    rand_input = torch.rand((batch_size * num_timesteps, *input_shape))
    out = dynapcnn_network(rand_input)

    qconfig = aquatic.utils.generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8, has_bias=has_bias
    )
    qdcnn = aquatic.prepare_qat(dynapcnn_network, qconfig=qconfig)
    qdcnn = dynapcnn_network

    out = qdcnn(rand_input)

    # Training loop
    optim = torch.optim.Adam(qdcnn.parameters())
    criterion = torch.nn.MSELoss()
    for i in range(10):
        optim.zero_grad()
        qdcnn.zero_grad()

        out = qdcnn(rand_input)
        loss = criterion(out.mean(), torch.tensor(1.0))
        loss.backward()

        optim.step()
