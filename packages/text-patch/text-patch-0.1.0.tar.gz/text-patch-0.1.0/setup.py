# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_patch']

package_data = \
{'': ['*'], 'text_patch': ['dict/*']}

install_requires = \
['edit-distance>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'text-patch',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Philip Huang',
    'author_email': 'p208p2002@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
