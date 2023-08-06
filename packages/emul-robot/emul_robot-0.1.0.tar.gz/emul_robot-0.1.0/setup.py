# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emul_robot']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=8.2.4,<9.0.0']

entry_points = \
{'console_scripts': ['robot = main']}

setup_kwargs = {
    'name': 'emul-robot',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Paul Choi',
    'author_email': 'straits9@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
