# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonalias']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonalias',
    'version': '0.1.1',
    'description': 'A microlibrary that defines a Json type alias for Python.',
    'long_description': None,
    'author': 'Kevin Heavey',
    'author_email': 'ID+username@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
