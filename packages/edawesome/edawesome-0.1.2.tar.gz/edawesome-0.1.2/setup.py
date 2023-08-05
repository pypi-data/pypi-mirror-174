# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edawesome']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.5.0,<9.0.0',
 'kaggle>=1.5.12,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'transitions>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'edawesome',
    'version': '0.1.2',
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
