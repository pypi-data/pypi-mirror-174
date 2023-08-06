# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argument_checks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argument-checks',
    'version': '0.1.0',
    'description': 'utility for checking that call args have the expected types and all required args are provided',
    'long_description': None,
    'author': 'Julian Heise',
    'author_email': 'jam.heise@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
