# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usabrewer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usabrewer',
    'version': '0.0.4',
    'description': 'Python color palettes based on travel posters from the 50 states',
    'long_description': '',
    'author': 'Emma Glass',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
