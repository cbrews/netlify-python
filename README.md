# Netlify Python Client SDK

![GitHub release (latest by date)](https://img.shields.io/github/v/release/cbrews/netlify-python?label=netlify-python)
[![CI](https://github.com/cbrews/netlify-python/actions/workflows/ci.yml/badge.svg)](https://github.com/cbrews/netlify-python/actions/workflows/ci.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netlify-python)
![PyPI - License](https://img.shields.io/pypi/l/netlify-python)

This is a work in progress package designed to wrap the [Netlify APIs](https://docs.netlify.com/api/get-started/) for python client users.

Note that this library is in pre-release and the APIs may be changed in later versions.

## User Guide

This section is intended for developers who want to use the library to make requests to Netlify.

### Installation

⚠ `netlify-python` currently supports python 3.10+.

Recommended installation through [PIP](https://pypi.org/project/netlify-python/) via pypi.

```shell
$ pip install netlify-python
```

### Usage

This client currently only supports [Personal Access Tokens](https://app.netlify.com/user/applications#personal-access-tokens).  Navigate to User Settings > Applications > Personal Access Tokens and create a new access token.  This is the token you'll use in your initialization of the client.

This created a client that can send http requests.

```python
from netlify import NetlifyClient

client = NetlifyClient(access_token="my-access-token")

client.get_current_user() # Get current user information
client.create_site_deploy('site-id', 'path/to/zip/file.zip')
```

### API

⚠ This client is currently expanding its API support, more documentation coming soon here.

## For Developers

This section is for developers who want to improve this library.  The default development version is on 3.10.4 but we are currently supporting all python versions >= 3.10

### Development Dependencies

Make sure that you have [`pyenv`](https://github.com/pyenv/pyenv).  You can test this by checking your python version after opening this directory.

```bash
$ python --version
Python 3.10.4
```

Make sure your active python version has `virtualenv` setup via:

```bash
$ python -m pip install virtualenv
```

Create and activate your venv
```bash
$ python -m venv venv
$ . venv/bin/activate
```

### Starting development

Everything here out should be in the venv.

Install your dependencies:
```bash
$ pip install .[dev]
```

Setup pre-commits:
```bash
$ pre-commit install
```

You should be good to go now.

### Building the package
Get your build dependencies in place:

```bash
$ pip install .[build]
```

Then build the package:
```bash
$ python -m build
```
