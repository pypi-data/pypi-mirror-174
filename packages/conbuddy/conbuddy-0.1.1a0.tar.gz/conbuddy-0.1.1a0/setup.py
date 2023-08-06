# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conbuddy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'conbuddy',
    'version': '0.1.1a0',
    'description': 'The conbuddy package makes it easy to manage environment specific configuration values.',
    'long_description': '# conbuddy\n\nThe conbuddy package makes it easy to manage environment specific configuration values. Inspired by <https://rstudio.github.io/config/articles/introduction.html>.\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/samedwardes/conbuddy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
