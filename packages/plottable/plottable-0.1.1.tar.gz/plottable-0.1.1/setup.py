# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plottable']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'plottable',
    'version': '0.1.1',
    'description': 'most pretty & lovely tables with matplotlib',
    'long_description': 'None',
    'author': 'znstrider',
    'author_email': 'mindfulstrider@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/znstrider/plottable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
