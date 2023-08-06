# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statute_utils', 'statute_utils.formula']

package_data = \
{'': ['*'], 'statute_utils': ['docs/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.2,<2.0.0',
 'text-gists>=0.0.2,<0.0.3']

setup_kwargs = {
    'name': 'statute-utils',
    'version': '0.0.13',
    'description': 'Helper functions for statutory processing.',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
