# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['movieparse']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['movieparse = movieparse.cli:main']}

setup_kwargs = {
    'name': 'movieparse',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'schuenemann',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
