# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edawesome']

package_data = \
{'': ['*']}

install_requires = \
['kaggle>=1.5.12,<2.0.0', 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'edawesome',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Timofei Ryko',
    'author_email': 'timofei.ryko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
