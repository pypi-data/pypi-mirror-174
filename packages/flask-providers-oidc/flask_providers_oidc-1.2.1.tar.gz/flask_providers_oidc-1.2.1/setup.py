# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_oidc']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0', 'oauth2client>=4.1.3,<5.0.0']

entry_points = \
{'console_scripts': ['oidc-register = flask_oidc.registration_util:main']}

setup_kwargs = {
    'name': 'flask-providers-oidc',
    'version': '1.2.1',
    'description': 'Fork version flask oidc',
    'long_description': '# flask-oidc\n\n## Forked Version\n\n[![image](https://img.shields.io/pypi/v/flask-providers-oidc.svg?style=flat)](https://pypi.python.org/pypi/flask-providers-oidc)![https://github.com/benbenbang/flask-oidc/actions/workflows/wf-ci.yml/badge.svg&flat](https://github.com/benbenbang/flask-oidc/actions/workflows/wf-ci.yml/badge.svg) ![https://img.shields.io/pypi/pyversions/flask-providers-oidc](https://img.shields.io/pypi/pyversions/flask-providers-oidc) ![https://img.shields.io/pypi/format/flask-providers-oidc&flat](https://img.shields.io/pypi/format/flask-providers-oidc) ![https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&flat)\n\nThis project is forked from [flask-oidc](https://github.com/puiterwijk/flask-oidc), and is now renamed **flask-providers-oidc**\n\nThis version uses `pyjwt` instead of `isdangerous`.\n\nNo need to change the import:\n\n```python\nfrom oidc import OpenIDConnect\n...\n```\n\n## Description\n\n[OpenID Connect](https://openid.net/connect/) support for [Flask](http://flask.pocoo.org/).\n\nThis library should work with any standards-compliant OpenID Connect provider.\n\nIt has been tested with:\n\n-   [Google+ Login](https://developers.google.com/accounts/docs/OAuth2Login)\n-   [Ipsilon](https://ipsilon-project.org/)\n',
    'author': 'benbenbang',
    'author_email': 'bn@benbenbang.io',
    'maintainer': 'benbenbang',
    'maintainer_email': 'bn@benbenbang.io',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
