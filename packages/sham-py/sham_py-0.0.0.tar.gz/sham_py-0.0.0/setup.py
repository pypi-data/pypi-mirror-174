# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'sham-py',
    'version': '0.0.0',
    'description': 'A simple yet shit Discord API wrapper',
    'long_description': '# Sham.py\n\nA simple yet shit Discord API wrapper for Python\n',
    'author': 'Enoki',
    'author_email': 'enokiun@gmail.com',
    'maintainer': 'EnokiUN',
    'maintainer_email': 'enokiun@gmail.com',
    'url': 'https://github.com/EnokiUN/sham.py',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
