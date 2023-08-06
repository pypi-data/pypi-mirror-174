# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_automation']

package_data = \
{'': ['*']}

install_requires = \
['appium-python-client>=2.7.1,<3.0.0',
 'pytest>=7.2.0,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'selenium>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'test-automation',
    'version': '0.1.4',
    'description': 'test framework for yogiyo',
    'long_description': 'None',
    'author': 'KimKitaeB',
    'author_email': 'kt.kim@wesang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
