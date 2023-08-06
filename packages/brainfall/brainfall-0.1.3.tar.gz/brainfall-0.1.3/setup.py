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
    'version': '0.1.3',
    'description': '',
    'long_description': '## hello world\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![][versions-image]][versions-url]\n\n[pypi-image]: https://img.shields.io/pypi/v/brainfall\n[pypi-url]: https://pypi.org/project/brainfall\n[build-image]: https://github.com/eliaonceagain/brainfall/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/eliaonceagain/brainfall/actions/workflows/build.yaml\n[coverage-image]: https://codecov.io/gh/eliaonceagain/brainfall/branch/master/graph/badge.svg?token=RSKB6B6WD4\n[coverage-url]: https://codecov.io/gh/eliaonceagain/brainfall\n[versions-image]: https://img.shields.io/pypi/pyversions/brainfall\n[versions-url]: https://pypi.org/project/brainfall\n',
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
