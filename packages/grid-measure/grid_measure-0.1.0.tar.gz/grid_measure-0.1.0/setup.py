# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grid_measure']

package_data = \
{'': ['*']}

install_requires = \
['cloup>=1.0.1,<2.0.0',
 'deskew>=1.3.3,<2.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['grid_measure = grid_measure.cli:cli']}

setup_kwargs = {
    'name': 'grid-measure',
    'version': '0.1.0',
    'description': 'A tool for measuring the scale of grid paper.',
    'long_description': None,
    'author': 'TankredO',
    'author_email': 'tankred.ott@ur.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
