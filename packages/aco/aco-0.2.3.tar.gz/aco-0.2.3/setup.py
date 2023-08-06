# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aco',
    'version': '0.2.3',
    'description': 'Ant Colony Optimization in Python',
    'long_description': '# Ant Colony Optimization\n\n##### Implementation of the Ant Colony Optimization algorithm in Python\n\n> Currently works on 2D Cartesian coordinate system\n\n## Installation\n\n#### From PyPi\n\n```shell\npip install aco\n```\n\n#### Using [Poetry](https://python-poetry.org/)\n\n```shell\npoetry add aco\n```\n\n## Usage\n\n```python\nAntColony(\n    nodes,\n    start=None,\n    ant_count=300,\n    alpha=0.5,\n    beta=1.2,\n    pheromone_evaporation_rate=0.40,\n    pheromone_constant=1000.0,\n    iterations=300,\n)\n```\n\n### Travelling Salesman Problem\n```python\nimport matplotlib.pyplot as plt\nimport random\n\nfrom aco import AntColony\n\n\nplt.style.use("dark_background")\n\n\nCOORDS = (\n    (20, 52),\n    (43, 50),\n    (20, 84),\n    (70, 65),\n    (29, 90),\n    (87, 83),\n    (73, 23),\n)\n\n\ndef random_coord():\n    r = random.randint(0, len(COORDS))\n    return r\n\n\ndef plot_nodes(w=12, h=8):\n    for x, y in COORDS:\n        plt.plot(x, y, "g.", markersize=15)\n    plt.axis("off")\n    fig = plt.gcf()\n    fig.set_size_inches([w, h])\n\n\ndef plot_all_edges():\n    paths = ((a, b) for a in COORDS for b in COORDS)\n\n    for a, b in paths:\n        plt.plot((a[0], b[0]), (a[1], b[1]))\n\n\nplot_nodes()\n\ncolony = AntColony(COORDS, ant_count=300, iterations=300)\n\noptimal_nodes = colony.get_path()\n\nfor i in range(len(optimal_nodes) - 1):\n    plt.plot(\n        (optimal_nodes[i][0], optimal_nodes[i + 1][0]),\n        (optimal_nodes[i][1], optimal_nodes[i + 1][1]),\n    )\n\n\nplt.show()\n```\n\n![screenshot](screenshot.jpg)\n\n---\n\n#### Reference\n\n- [Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)\n\n- [pjmattingly/ant-colony-optimization](https://github.com/pjmattingly/ant-colony-optimization)\n',
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
