# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['license_manager']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=38.0.2,<39.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['qxlicense = license_manager.main:main']}

setup_kwargs = {
    'name': 'license-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'leaf',
    'author_email': 'ncoder@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
