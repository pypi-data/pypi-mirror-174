# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basic_uncenter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basic-uncenter',
    'version': '0.2',
    'description': 'Basic math, printing, and text formatting.',
    'long_description': None,
    'author': 'uncenter',
    'author_email': 'uncenteristaken@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
