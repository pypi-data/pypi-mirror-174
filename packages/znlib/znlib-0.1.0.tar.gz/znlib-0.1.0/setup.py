# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['znlib', 'znlib.atomistic', 'znlib.examples']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0']

extras_require = \
{'atomistic': ['zntrack>=0.4.3,<0.5.0', 'ase>=3.22.1,<4.0.0'],
 'zntrack': ['zntrack>=0.4.3,<0.5.0', 'matplotlib>=3.6.1,<4.0.0']}

entry_points = \
{'console_scripts': ['znlib = znlib.cli:znlib_status']}

setup_kwargs = {
    'name': 'znlib',
    'version': '0.1.0',
    'description': '',
    'long_description': '# znlib\nThis package provides you with a CLI to list your installed zincware libraries.\n\nWhen installing via `pip install znlib[zntrack]` your output should look something like:\n\n```\n>>> znlib\nAvailable zincware packages:\n  ✓  znlib       (0.1.0)\n  ✓  zntrack     (0.4.3)\n  ✗  mdsuite \n  ✓  znjson      (0.2.1)\n  ✓  zninit      (0.1.1)\n  ✓  dot4dict    (0.1.1)\n  ✗  znipy \n  ✗  supercharge \n  ✗  znvis \n  ✗  symdet \n```\n\nFurthermore, `znlib` provides you with some example [ZnTrack](https://github.com/zincware/ZnTrack) Nodes.\n\n```python\nfrom znlib.examples import MonteCarloPiEstimator\n\nmcpi = MonteCarloPiEstimator(n_points=1000).write_graph(run=True)\nprint(mcpi.load().estimate)\n>>> 3.128\n```\n\nThe idea of the `znlib` package is to provide a collection of [ZnTrack](https://github.com/zincware/ZnTrack) Nodes from all different fields of research.\nEvery contribution is very welcome.\nFor new Nodes:\n1. Fork this repository.\n2. Create a file under the directory `znlib/examples`\n3. Make a Pull request.\n\n',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
