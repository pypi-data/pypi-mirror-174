# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_session']

package_data = \
{'': ['*']}

install_requires = \
['pylibmc>=1.6.3,<2.0.0']

extras_require = \
{'all': ['cachelib>=0.9.0',
         'pymongo>=4.3.2',
         'redis>=4.3.4',
         'flask-sqlalchemy>=1.0.0'],
 'cache': ['cachelib>=0.9.0'],
 'mongo': ['pymongo>=4.3.2'],
 'redis': ['redis>=4.3.4'],
 'sqlalechmey': ['flask-sqlalchemy>=1.0.0']}

setup_kwargs = {
    'name': 'flask-providers-session',
    'version': '0.4.1',
    'description': 'Fork version flask session',
    'long_description': 'Flask-Session\n=============\n\n## Forked Version\n\n[![image](https://img.shields.io/pypi/v/flask-providers-session.svg?style=flat)](https://pypi.python.org/pypi/flask-providers-session)![https://github.com/benbenbang/flask-session/actions/workflows/wf-ci.yml/badge.svg&flat](https://github.com/benbenbang/flask-oidc/actions/workflows/wf-ci.yml/badge.svg) ![https://img.shields.io/pypi/pyversions/flask-providers-session](https://img.shields.io/pypi/pyversions/flask-providers-session) ![https://img.shields.io/pypi/format/flask-providers-session&flat](https://img.shields.io/pypi/format/flask-providers-session) ![https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&flat)\n\nThis project is forked from [flask-session](https://github.com/fengsp/flask-session), and is now renamed **flask-providers-session**. Flask-Session is an extension for Flask that adds support for Server-side sessions to your application.\n\nNote that this version stops supporting python 2.\n',
    'author': 'benbenbang',
    'author_email': 'bn@benbenbang.io',
    'maintainer': 'benbenbang',
    'maintainer_email': 'bn@benbenbang.io',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
