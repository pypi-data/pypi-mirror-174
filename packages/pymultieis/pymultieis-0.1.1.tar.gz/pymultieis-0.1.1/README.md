
# pymultieis

[**Installation**](#installation)
| [**Examples**](https://github.com/richinex/pymultieis/tree/main/docs/source/examples)
| [**Documentation**](https://pymultieis.readthedocs.io/en/latest/index.html)
| [**Citing this work**](#citation)


A library for fitting a sequence of electrochemical impedance spectra (PyTorch version).

- Implements algorithms for simultaneous and sequential fitting.

- Written in python and based on the [PyTorch](https://pytorch.org/) library.

- Leverages deterministic solvers from [pytorch-minimize](https://pytorch-minimize.readthedocs.io/en/latest/api/index.html) which compute the first- and second-order derivatives via autograd.

## Installation<a id="installation"></a>

Installation of pymultieis should be done via pip:

```bash
pip install pymultieis
```

[Getting started with pymultieis](https://pymultieis.readthedocs.io/en/latest/quick-start-guide.html#) contains a quick start guide to
fitting your data with ``pymultieis``.


## Examples

Jupyter notebooks which cover several aspects of ``pymultieis`` can be found in [Examples](https://github.com/richinex/pymultieis/tree/main/docs/source/examples).

## Documentation

Details about the ``pymultieis`` API, can be found in the [reference documentation](https://pymultieis.readthedocs.io/en/latest/index.html).


## Citing this work<a id="citation"></a>

If you use pymultieis for academic research, you may cite the library as follows:

```
@misc{Chukwu2022,
  author = {Chukwu, Richard},
  title = {pymultieis: a library for fitting a sequence of electrochemical impedance spectra},
  publisher = {GitHub},
  year = {2022},
  url = {https://github.com/richinex/pymultieis},
}
```