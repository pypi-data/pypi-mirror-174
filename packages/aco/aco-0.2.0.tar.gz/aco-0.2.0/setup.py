# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aco',
    'version': '0.2.0',
    'description': 'Ant Colony Optimization in Python',
    'long_description': 'None',
    'author': 'Harish',
    'author_email': 'harishhari3112004@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
