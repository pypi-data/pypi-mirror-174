![aquatic](docs/_static/Logo_white_background.png)

## Another Quantization-aware Training Library for PyTorch?

The default quantization implementations in [pytorch](https://pytorch.org/docs/stable/quantization.html) or [BNN](https://github.com/1adrianb/binary-networks-pytorch) are very opinionated in terms of which parameters are quantized and which ones are not.

This library aims to make it fully flexible in terms of which types of quantizations are possible and which parameters are to be quantized.

## Game plan

The quantization specifications are specified in pytorch libraries through a `qconfig`/`bconfig` which is a struct or a dictionary with a given set of methods specifying methods that are used and called for quantizing the various parameters and tensors in the computational graph.

So we will augment the QConfig with additional attributes for biases, time constants (and perhaps generalize to all parameters?).

We will start with an implementation that works and then slowly migrate towards as many primitives as we can borrow from `pytorch`.

## Motivation and Ideas

After digging through most of the `pytorch` github repository to understand its quantization pipeline with no success, `BNN`(https://github.com/1adrianb/binary-networks-pytorch) implementation came to my rescue and helped understand the workflow a bit better.

## API fundamentals

### QConfig

The quantization parameters are described by the `QConfig` object which has the following attributes:
- `activation`: A `class` containing all details pertaining to quantization of activation.
- `weight`: A `class` containing all details pertaining to quantization of `weight` parameter.
- `bias`: A `class` containing all details pertaining to quantization of `bias` parameter.
- `tau`: A `class` containing all the details pertaining to quantization of `tau` or time constants.
- `alpha`: A `class` containing all the details pertaining to quantization of `alpha` corresponding to the decay factor of a given state.

### The `.nn` submodule

The `.nn` submodule here depicts all the classes that are quantization aware equivalents of the non-quantized classes.
These classes inherrently follow the following data-flow.

1. Quantized data (still a float tensor) as provided as input
2. If the class has any parameters corresponding to `weight` or `bias` or `tau`, they will all be quantized based on the `QConfig` instance `qconfig` attached to it.
3. The class does it's forward pass with the quantized parameters.
4. The activation of this class is then quantized based on the `QConfig` specification.
5. The output is produced.

### Pre-commit
If you want to use automatic `Black` formatting before every git commit, you'll need to install `pre-commit`:
```
pip install pre-commit
```

And then install the pre-commit hooks in the repository root:
```
pre-commit install
```