# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aco',
    'version': '0.2.1',
    'description': 'Ant Colony Optimization in Python',
    'long_description': '# Ant Colony Optimization\n\n#### Implementation of the Ant Colony Optimization algorithm in Python\n\n#### Reference\n+ [Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)\n',
    'author': 'Harish',
    'author_email': 'harishhari3112004@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/harish3124/aco',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
