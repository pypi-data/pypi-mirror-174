# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['stream_tui']
install_requires = \
['blessed>=1.19.1,<2.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'stream-tui',
    'version': '0.5.0',
    'description': 'Easily create pretty user interfaces for your CLI apps',
    'long_description': '# Stream TUI',
    'author': 'Jakob Pinterits',
    'author_email': 'jakob.pinterits@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
