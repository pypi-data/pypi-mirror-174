# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['more_pyspark']

package_data = \
{'': ['*']}

install_requires = \
['composable>=0.2.5,<0.3.0',
 'more-itertools>=9.0.0,<10.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pyspark>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'more-pyspark',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Todd Iverson',
    'author_email': 'Tiverson@winona.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
