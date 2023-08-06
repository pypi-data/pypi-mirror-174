# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sui_sdk', 'sui_sdk.cryptography']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0',
 'hdwallet>=2.1.1,<3.0.0',
 'mnemonic>=0.20,<0.21',
 'secp256k1>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'sui-sdk',
    'version': '0.1.1.dev0',
    'description': 'Sui client library for the Python language',
    'long_description': None,
    'author': 'overcat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
