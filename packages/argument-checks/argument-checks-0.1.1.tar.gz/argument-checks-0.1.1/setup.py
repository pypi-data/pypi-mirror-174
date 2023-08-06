# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argument_checks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'argument-checks',
    'version': '0.1.1',
    'description': 'utility for checking that call args have the expected types and all required args are provided',
    'long_description': '# Arg Check\n\nA Python utility for checking that call args have the expected types and all required args are provided.\n\n**Works only with Python 3.7** (fixing that soon)\n\n## Installation\n\n```commandline\npip install arg-check\n```\n\n## Usage\n\nThis library uses simple decorators.\n\n### Argument Type Checking\n\n```Python\n@enforce_arg_types\ndef foobar(a: int, b: str):\n    ...\n```\n\n- Type checking is performed via the annotations. If an argument does not have an\n  annotation, type checking is skipped just for that argument.\n- If an argument is a collection, all items in the collection are checked.\n- Can handle `Union` and `Optional`\n\n### Required Arguments\n\n```Python\n@required_args("a", "b")\ndef foobar(a, b, c=None):\n    ...\n```\n\n- Tests the given arguments and raises a `ValueError` if the value is either\n  `None` or an empty string\n- To make all arguments required, use `@required_args` without parenthesis\n\n### All checks in one decorator\n\n```Python\n@strict_args\ndef foobar(a: int, b: str):\n    ...\n```\n\n- All arguments are type checked\n- All arguments are required\n',
    'author': 'Julian Heise',
    'author_email': 'jam.heise@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/juheise/argument-checks/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
