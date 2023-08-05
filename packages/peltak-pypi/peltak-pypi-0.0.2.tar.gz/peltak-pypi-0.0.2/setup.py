# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['peltak_pypi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'peltak-pypi',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Mateusz Klos',
    'author_email': 'novopl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://novopl.github.io/peltak-pypi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
