# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['puloon']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0', 'tabulate>=0.9.0,<0.10.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['puloon = puloon.cli:app']}

setup_kwargs = {
    'name': 'puloon',
    'version': '0.1.1',
    'description': '',
    'long_description': '### Puloon LCDM-4000\n\nThe document is related to the communication protocol of LCDM-4000, which is made by Puloon Technology.\n',
    'author': 'Aibek',
    'author_email': 'aiba.kg93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
