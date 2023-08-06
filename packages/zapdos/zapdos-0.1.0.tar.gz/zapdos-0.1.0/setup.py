# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zapdos']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'zapdos',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Joseph Chu',
    'author_email': 'josephchu21@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
