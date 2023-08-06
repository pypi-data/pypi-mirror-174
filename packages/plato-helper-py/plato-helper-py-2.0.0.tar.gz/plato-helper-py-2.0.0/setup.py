# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plato_helper_py']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2,<3.0', 'requests>=2.27,<3.0', 'types-requests>=2.28.11,<3.0.0']

setup_kwargs = {
    'name': 'plato-helper-py',
    'version': '2.0.0',
    'description': 'Helper for the Plato microservice',
    'long_description': None,
    'author': 'Tiago Santos',
    'author_email': 'tiago.santos@vizidox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.10',
}


setup(**setup_kwargs)
