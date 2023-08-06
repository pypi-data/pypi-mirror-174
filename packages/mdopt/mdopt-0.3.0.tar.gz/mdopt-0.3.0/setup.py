# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdopt', 'mdopt.contractor', 'mdopt.mps', 'mdopt.optimiser', 'mdopt.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0',
 'more-itertools>=8.12,<10.0',
 'numpy>=1.20.1,<2.0.0',
 'opt-einsum>=3.3.0,<4.0.0',
 'qecstruct>=0.2.9,<0.3.0',
 'scipy>=1.9.2,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'mdopt',
    'version': '0.3.0',
    'description': 'Discrete optimization in the tensor-network (specifically, MPS-MPO) language.',
    'long_description': 'None',
    'author': 'Aleksandr Berezutskii',
    'author_email': 'berezutskii@phystech.edu',
    'maintainer': 'Aleksandr Berezutskii',
    'maintainer_email': 'berezutskii@phystech.edu',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
