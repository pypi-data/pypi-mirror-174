# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaussidan']

package_data = \
{'': ['*']}

install_requires = \
['lmfit>=1.0.3,<2.0.0', 'numpy>=1.23.2,<2.0.0']

setup_kwargs = {
    'name': 'gaussidan',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Daniel Williams',
    'author_email': 'daniel.mays.williams@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
