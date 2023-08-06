# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rumex', 'rumex.parsing', 'rumex.parsing.state_machine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rumex',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'uigctaw',
    'author_email': 'uigctaw@metadata.social',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
