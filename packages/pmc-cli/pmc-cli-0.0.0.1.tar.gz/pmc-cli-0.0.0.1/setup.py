# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pmc = pmc.main:run']}

setup_kwargs = {
    'name': 'pmc-cli',
    'version': '0.0.0.1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
