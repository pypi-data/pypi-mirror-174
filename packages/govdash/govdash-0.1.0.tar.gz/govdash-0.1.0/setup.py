# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['govdash']

package_data = \
{'': ['*']}

install_requires = \
['dash>=2.6.2,<3.0.0']

setup_kwargs = {
    'name': 'govdash',
    'version': '0.1.0',
    'description': 'Gov styled components for Dash',
    'long_description': '# govdash\n\nA UK Gov-styled component library for Dash.\n',
    'author': 'ellsphillips',
    'author_email': 'elliott.phillips.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ellsphillips/govdash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
