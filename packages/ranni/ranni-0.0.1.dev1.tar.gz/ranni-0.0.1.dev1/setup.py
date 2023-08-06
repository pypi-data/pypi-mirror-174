# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ranni']

package_data = \
{'': ['*']}

install_requires = \
['beartype', 'semantic-version']

setup_kwargs = {
    'name': 'ranni',
    'version': '0.0.1.dev1',
    'description': 'Simple, composable and scalable command line interface library',
    'long_description': 'ranni\n=====\n\nSimple, composable and scalable command line interface library\n',
    'author': 'ddnomad',
    'author_email': 'self@ddnomad.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ddnomad/ranni',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
