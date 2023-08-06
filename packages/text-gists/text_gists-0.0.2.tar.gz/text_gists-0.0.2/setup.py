# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_gists']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'text-gists',
    'version': '0.0.2',
    'description': 'Helper functions for matching regex and other text-based patterns.',
    'long_description': '# Regex Gists\n\nHelper functions for matching regex and other text-based patterns.\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
