# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ton_node_control',
 'ton_node_control.cli',
 'ton_node_control.cli.utils',
 'ton_node_control.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0', 'click==8.1.3', 'mypy==0.982', 'pytest==7.2.0', 'toml==0.10.2']

setup_kwargs = {
    'name': 'ton-node-control',
    'version': '0.0.1.1',
    'description': '',
    'long_description': '# ton-node-control\n',
    'author': 'Alexander Walther',
    'author_email': 'asushofman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Walther-s-Engineering/ton-node-control',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
