# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncsqlite']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'asyncsqlite',
    'version': '0.1.4',
    'description': '',
    'long_description': '# asyncsqlite\nAn async sqlite library with pooling support\n\n## Requirements\nPython 3.7.2+\n## Installation\n* `pip install asyncsqlite`\n#\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Snowie-ORG/asyncsqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
