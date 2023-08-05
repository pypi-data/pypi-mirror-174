# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trendlist']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.1,<2.0.0',
 'myst-parser>=0.18.1,<0.19.0',
 'sphinx-autobuild>=2021.3.14,<2022.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'sphinx>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'trendlist',
    'version': '0.1.13',
    'description': 'Define, manipulate and study lists of Trends.',
    'long_description': None,
    'author': 'Jeffrey S. Haemer',
    'author_email': 'jeffrey.haemer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
