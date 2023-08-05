# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liquidbase', 'liquidbase.api', 'liquidbase.db']

package_data = \
{'': ['*']}

install_requires = \
['Pympler>=1.0.1,<2.0.0',
 'SQLAlchemy>=1.4.42,<2.0.0',
 'asciitree>=0.3.3,<0.4.0',
 'dill>=0.3.6,<0.4.0',
 'numpy>=1.23.4,<2.0.0',
 'orjson>=3.8.1,<4.0.0',
 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'liquidbase',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Mikkel Vilstrup',
    'author_email': 'mikkel@vilstrup.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
