# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_metadata_client']

package_data = \
{'': ['*']}

install_requires = \
['sgqlc>=16.0,<17.0']

setup_kwargs = {
    'name': 'dbt-metadata-client',
    'version': '0.1.0',
    'description': "A simple python client for interacting with dbt's metadata API",
    'long_description': '',
    'author': 'Transform',
    'author_email': 'hello@transformdata.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
