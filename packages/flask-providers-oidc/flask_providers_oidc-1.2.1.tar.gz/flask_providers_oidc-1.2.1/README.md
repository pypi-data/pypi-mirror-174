# flask-oidc

## Forked Version

[![image](https://img.shields.io/pypi/v/flask-providers-oidc.svg?style=flat)](https://pypi.python.org/pypi/flask-providers-oidc)![https://github.com/benbenbang/flask-oidc/actions/workflows/wf-ci.yml/badge.svg&flat](https://github.com/benbenbang/flask-oidc/actions/workflows/wf-ci.yml/badge.svg) ![https://img.shields.io/pypi/pyversions/flask-providers-oidc](https://img.shields.io/pypi/pyversions/flask-providers-oidc) ![https://img.shields.io/pypi/format/flask-providers-oidc&flat](https://img.shields.io/pypi/format/flask-providers-oidc) ![https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&flat)

This project is forked from [flask-oidc](https://github.com/puiterwijk/flask-oidc), and is now renamed **flask-providers-oidc**

This version uses `pyjwt` instead of `isdangerous`.

No need to change the import:

```python
from oidc import OpenIDConnect
...
```

## Description

[OpenID Connect](https://openid.net/connect/) support for [Flask](http://flask.pocoo.org/).

This library should work with any standards-compliant OpenID Connect provider.

It has been tested with:

-   [Google+ Login](https://developers.google.com/accounts/docs/OAuth2Login)
-   [Ipsilon](https://ipsilon-project.org/)
