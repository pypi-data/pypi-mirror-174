# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brainfall',
 'brainfall.markets',
 'brainfall.models',
 'brainfall.models.binance',
 'brainfall.utils']

package_data = \
{'': ['*']}

install_requires = \
['binance-connector>=1.18.0,<2.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'brainfall',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'EliaOnceAgain',
    'author_email': 'eabunassar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
