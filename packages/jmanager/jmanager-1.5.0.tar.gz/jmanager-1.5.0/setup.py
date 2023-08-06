# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jmanager']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'jupyterlab>=3.1.4,<4.0.0']

entry_points = \
{'console_scripts': ['jmanager = jmanager.cli:main']}

setup_kwargs = {
    'name': 'jmanager',
    'version': '1.5.0',
    'description': 'A lightweight Jupyter process manager',
    'long_description': '# Jmanager\n\nA lightweight Jupyter process manager\n\n## todo\nWrite docs.\n',
    'author': 'Yasunori Horikoshi',
    'author_email': 'horikoshi.et.al@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotoku/jmanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
