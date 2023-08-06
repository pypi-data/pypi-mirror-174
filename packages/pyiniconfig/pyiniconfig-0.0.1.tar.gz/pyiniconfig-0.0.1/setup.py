# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyiniconfig']
setup_kwargs = {
    'name': 'pyiniconfig',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Xenely',
    'author_email': 'a.maryatkin14@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
