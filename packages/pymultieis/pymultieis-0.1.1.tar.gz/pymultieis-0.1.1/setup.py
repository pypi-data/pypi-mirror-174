# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymultieis']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib==3.5',
 'numpy==1.23.1',
 'pandas>=1.4.4,<2.0.0',
 'pytorch-minimize>=0.0.2,<0.0.3',
 'scipy==1.9.3',
 'torch>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'pymultieis',
    'version': '0.1.1',
    'description': 'A library for fitting a sequence of electrochemical impedance spectra.',
    'long_description': '\n# pymultieis\n\n[**Installation**](#installation)\n| [**Examples**](https://github.com/richinex/pymultieis/tree/main/docs/source/examples)\n| [**Documentation**](https://pymultieis.readthedocs.io/en/latest/index.html)\n| [**Citing this work**](#citation)\n\n\nA library for fitting a sequence of electrochemical impedance spectra (PyTorch version).\n\n- Implements algorithms for simultaneous and sequential fitting.\n\n- Written in python and based on the [PyTorch](https://pytorch.org/) library.\n\n- Leverages deterministic solvers from [pytorch-minimize](https://pytorch-minimize.readthedocs.io/en/latest/api/index.html) which compute the first- and second-order derivatives via autograd.\n\n## Installation<a id="installation"></a>\n\nInstallation of pymultieis should be done via pip:\n\n```bash\npip install pymultieis\n```\n\n[Getting started with pymultieis](https://pymultieis.readthedocs.io/en/latest/quick-start-guide.html#) contains a quick start guide to\nfitting your data with ``pymultieis``.\n\n\n## Examples\n\nJupyter notebooks which cover several aspects of ``pymultieis`` can be found in [Examples](https://github.com/richinex/pymultieis/tree/main/docs/source/examples).\n\n## Documentation\n\nDetails about the ``pymultieis`` API, can be found in the [reference documentation](https://pymultieis.readthedocs.io/en/latest/index.html).\n\n\n## Citing this work<a id="citation"></a>\n\nIf you use pymultieis for academic research, you may cite the library as follows:\n\n```\n@misc{Chukwu2022,\n  author = {Chukwu, Richard},\n  title = {pymultieis: a library for fitting a sequence of electrochemical impedance spectra},\n  publisher = {GitHub},\n  year = {2022},\n  url = {https://github.com/richinex/pymultieis},\n}\n```',
    'author': 'Richard Chukwu',
    'author_email': 'richinex@gmail.com',
    'maintainer': 'Richard Chukwu',
    'maintainer_email': 'richinex@gmail.com',
    'url': 'https://github.com/richinex/pymultieis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
