import aquatic
import aquatic.nn as qnn
from aquatic.qconfig import QConfig
from aquatic.fake_quantize import FakeQuantize
from aquatic.quantizer import NoZeroShiftUniformStochasticRounding
from aquatic.observer import MinMaxObserver
import torch.nn as nn
import torch
import sinabs.layers as sl


qconfig = QConfig(
    weight=FakeQuantize.with_args(
        observer=MinMaxObserver,
        quantizer=NoZeroShiftUniformStochasticRounding(
            quant_min=-128,
            quant_max=127,
        ),
    ),
    bias=FakeQuantize.with_args(
        observer=MinMaxObserver,
        quantizer=NoZeroShiftUniformStochasticRounding(
            quant_min=-128,
            quant_max=127,
        ),
    ),
)


def test_linear_qparams():
    linear = qnn.Linear(20, 40, qconfig=qconfig)
    qparams = linear.quantize_params()

    assert (qparams["weight"] != linear.mod.weight).any()
    assert (qparams["bias"] != linear.mod.bias).any()


def test_linear_to_float():
    qlinear = qnn.Linear(20, 40, qconfig=qconfig)
    linear = qlinear.to_float()

    # TODO this should be .all(), but cannot use with StochasticRounding
    assert (linear.weight == qlinear.quantize_params()["weight"]).any()


def test_linear_from_float():
    linear = nn.Linear(2, 20)
    qlinear = qnn.Linear.from_float(mod=linear, qconfig=qconfig)

    assert qlinear.qconfig == qconfig
    assert (linear.weight == qlinear.mod.weight).all()


def test_conv_qparams():
    conv = qnn.Conv2d(1, 3, 3, qconfig=qconfig)
    qparams = conv.quantize_params()

    # TODO improve these assertions
    assert (qparams["weight"] != conv.mod.weight).any()
    assert (qparams["bias"] != conv.mod.bias).any()


def test_conv_to_float():
    qconv = qnn.Conv2d(1, 3, 3, qconfig=qconfig)
    conv = qconv.to_float()

    # TODO this should be .all(), but cannot use with StochasticRounding
    assert (conv.weight == qconv.quantize_params()["weight"]).any()


def test_conv_from_float():
    conv = nn.Conv2d(1, 3, 3)
    qconv = qnn.Conv2d.from_float(mod=conv, qconfig=qconfig)

    assert qconv.qconfig == qconfig
    assert (conv.weight == qconv.mod.weight).all()


def test_linear_backwards():
    qlinear = qnn.Linear(20, 40, qconfig=qconfig)
    rand_input = torch.rand((10, 20))
    output = qlinear(rand_input)
    output.sum().backward()


def test_conv_backwards():
    qconv = qnn.Conv2d(2, 3, 3, qconfig=qconfig)
    rand_input = torch.rand((10, 2, 3, 3))
    output = qconv(rand_input)
    output.sum().backward()
