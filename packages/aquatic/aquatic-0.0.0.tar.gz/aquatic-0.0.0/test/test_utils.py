from aquatic.utils import generate_dynapcnnlayer_qconfig
import pytest


@pytest.mark.parametrize("has_bias", [True, False])
def test_generate_dynapcnnlayer_qconfig(has_bias):
    qconfig = generate_dynapcnnlayer_qconfig(
        n_bits_weight=8, n_bits_threshold=8, has_bias=has_bias
    )
