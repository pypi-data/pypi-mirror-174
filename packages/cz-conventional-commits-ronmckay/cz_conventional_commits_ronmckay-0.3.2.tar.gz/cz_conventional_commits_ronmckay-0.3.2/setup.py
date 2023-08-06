# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cz_conventional_commits_ronmckay', 'conventional_commits_ronmckay_info']
install_requires = \
['commitizen>=2.37.0,<3.0.0']

setup_kwargs = {
    'name': 'cz-conventional-commits-ronmckay',
    'version': '0.3.2',
    'description': '',
    'long_description': '',
    'author': 'Philipp Oberdiek',
    'author_email': 'git@oberdiek.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
