# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sechat']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'requests>=2.27.0,<3.0.0',
 'websocket-client>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'sechat',
    'version': '1.1.0',
    'description': 'A BETTER Stack Exchange chat library.',
    'long_description': '# sechat\n[![Documentation Status](https://readthedocs.org/projects/sechat/badge/?version=latest)](https://sechat.readthedocs.io/en/latest/?badge=latest) [![Upload Python Package](https://github.com/GingerIndustries/sechat/actions/workflows/poetry.yml/badge.svg?event=release)](https://github.com/GingerIndustries/sechat/actions/workflows/poetry.yml)\n\nA _better_ Stack Exchange Chat library.\n\n[Documentation!](https://sechat.readthedocs.io/en/latest/)\n\nInstall from pypi using `pip install sechat`.\n',
    'author': 'Ginger',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
