# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mango']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['motor>=3.0.0,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'mango-odm',
    'version': '0.1.0',
    'description': '🥭 Async MongoDB ODM with type hints in Python',
    'long_description': '# Mango\n',
    'author': 'Akirami',
    'author_email': 'Akiramiaya@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/A-kirami/mango',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
