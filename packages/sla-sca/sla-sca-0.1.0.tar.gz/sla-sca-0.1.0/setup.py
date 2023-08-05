# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sla']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.6.0,<23.0.0',
 'earthengine-api>=0.1.316,<0.2.0',
 'geemap>=0.15.4,<0.16.0',
 'ipython>=8.4.0,<9.0.0',
 'sphinx>=5.3.0,<6.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'sla-sca',
    'version': '0.1.0',
    'description': 'Snow Line Altitude (SLA) monitoring for glaciers in Argentina.',
    'long_description': None,
    'author': 'Gurupratap Matharu',
    'author_email': 'gurupratap.matharu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
