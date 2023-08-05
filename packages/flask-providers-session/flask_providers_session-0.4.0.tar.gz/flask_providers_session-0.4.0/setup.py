# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_session']

package_data = \
{'': ['*']}

install_requires = \
['cachelib>=0.9.0,<0.10.0', 'pylibmc>=1.6.3,<2.0.0', 'pymongo>=4.3.2,<5.0.0']

setup_kwargs = {
    'name': 'flask-providers-session',
    'version': '0.4.0',
    'description': 'Fork version flask session',
    'long_description': 'Flask-Session\n=============\n\nFlask-Session is an extension for Flask that adds support for Server-side Session to your application.\n',
    'author': 'benbenbang',
    'author_email': 'ben.chen@vestiairecollective.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
