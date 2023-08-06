# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['potyk_fp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'potyk-fp',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
