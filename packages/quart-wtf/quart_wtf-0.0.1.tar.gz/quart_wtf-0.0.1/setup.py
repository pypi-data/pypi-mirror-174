# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quart_wtf']

package_data = \
{'': ['*']}

install_requires = \
['WTForms>=3.0.1,<4.0.0', 'quart>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'quart-wtf',
    'version': '0.0.1',
    'description': 'Simple integration of Quart and WTForms.',
    'long_description': '# Quart-WTF\n\n![Quart WTForms Logo](logos/logo.png)\n\nSimple integration of Quart and WTForms. Including CSRF and file uploading.\n',
    'author': 'Chris Rood',
    'author_email': 'quart.addons@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Quart-Addons/quart-uploads',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
