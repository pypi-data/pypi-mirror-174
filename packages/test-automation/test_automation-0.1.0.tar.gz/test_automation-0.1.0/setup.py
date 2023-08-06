# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_automation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-automation',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'KimKitaeB',
    'author_email': 'kt.kim@wesang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
