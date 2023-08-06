# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['math2eb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'math2eb',
    'version': '0.1.1',
    'description': 'A better math module for python',
    'long_description': None,
    'author': 'O.Plimer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
