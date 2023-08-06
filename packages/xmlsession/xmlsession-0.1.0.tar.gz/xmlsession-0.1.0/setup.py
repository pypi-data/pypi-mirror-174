# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xmlsession']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xmlsession',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Kalle R. Aagaard',
    'author_email': 'git@k-moeller.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KalleDK/py-xmlsession',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
