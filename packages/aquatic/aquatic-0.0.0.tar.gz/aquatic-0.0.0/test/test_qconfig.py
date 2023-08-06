import torch
import aquatic


def test_qconfig_init():
    from aquatic.qconfig import QConfig

    config = QConfig()

    data = torch.rand((2, 4))

    # Check the identity operation
    out = config.weight()(data)
    assert (out == data).all()
