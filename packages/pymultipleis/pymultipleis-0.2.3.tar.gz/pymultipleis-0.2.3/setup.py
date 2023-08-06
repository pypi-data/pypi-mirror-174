# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymultipleis']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.3.17,<0.4.0',
 'jaxopt==0.5.5',
 'matplotlib==3.6.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'scipy==1.9.1']

setup_kwargs = {
    'name': 'pymultipleis',
    'version': '0.2.3',
    'description': 'A library for fitting a sequence of electrochemical impedance spectra (JAX version).',
    'long_description': '\n# pymultipleis\n\n[**Installation**](#installation)\n| [**Examples**](https://github.com/richinex/pymultipleis/tree/main/docs/source/examples)\n| [**Documentation**](https://pymultipleis.readthedocs.io/en/latest/index.html)\n| [**Citing this work**](#citation)\n\n\nA library for fitting a sequence of electrochemical impedance spectra.\n\n- Implements algorithms for simultaneous and sequential fitting.\n\n- Written in python and based on the [JAX library](https://github.com/google/jax).\n\n- Leverages JAX\'s in-built automatic differentiation ([autodiff](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html)) of Python functions.\n\n- Takes advantage of JAX\'s just-in-time compilation (JIT) of Python code to [XLA](https://www.tensorflow.org/xla) which runs on GPU or TPU hardware.\n\n\n## Installation<a id="installation"></a>\n\npymultipleis requires the following:\n\n-   Python (>=3.9)\n-   [JAX](https://jax.readthedocs.io/en/latest/) (>=0.3.17)\n\nInstalling JAX on Linux is natively supported by the JAX team and instructions to do so can be found [here](https://github.com/google/jax#installation).\n\nFor Windows systems, the officially supported method is building directly from the source code (see [Building JAX from source](https://jax.readthedocs.io/en/latest/developer.html#building-from-source)).\nHowever, it might be easier to use pre-built JAX wheels which can be found in this [Github repo](https://github.com/cloudhan/jax-windows-builder). Further details\non Windows installation is also provided in this [repo](https://github.com/Dipolar-Quantum-Gases/jaxfit/blob/main/README.md).\n\n\nAfter installing JAX, you can now install pymultipleis via the following pip command\n\n```bash\npip install pymultipleis\n```\n\n[Getting started with pymultipleis](https://pymultipleis.readthedocs.io/en/latest/quick-start-guide.html#) contains a quick start guide to\nfitting your data with ``pymultipleis``.\n\n\n## Examples\n\nJupyter notebooks which cover several aspects of ``pymultipleis`` can be found in [Examples](https://github.com/richinex/pymultipleis/tree/main/docs/source/examples).\n\n## Documentation\n\nDetails about the ``pymultipleis`` API, can be found in the [reference documentation](https://pymultipleis.readthedocs.io/en/latest/index.html).\n\n\n## Citing this work<a id="citation"></a>\n\nIf you use pymultipleis for academic research, you may cite the library as follows:\n\n```\n@misc{Chukwu2022,\n  author = {Chukwu, Richard},\n  title = {pymultipleis: a library for fitting a sequence of electrochemical impedance spectra},\n  publisher = {GitHub},\n  year = {2022},\n  url = {https://github.com/richinex/pymultipleis},\n}\n```',
    'author': 'Richard Chukwu',
    'author_email': 'richinex@gmail.com',
    'maintainer': 'Richard Chukwu',
    'maintainer_email': 'richinex@gmail.com',
    'url': 'https://github.com/richinex/pymultipleis',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
