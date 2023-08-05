# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coshiota']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.2', 'orjson>=3.7.12,<4.0.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'coshiota',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'doubleO8',
    'author_email': 'wb008@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
