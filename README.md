# Netlify Python Client SDK

![GitHub release (latest by date)](https://img.shields.io/github/v/release/cbrews/netlify-python?label=netlify-python)
[![CI](https://github.com/cbrews/netlify-python/actions/workflows/ci.yml/badge.svg)](https://github.com/cbrews/netlify-python/actions/workflows/ci.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netlify-python)
![PyPI - License](https://img.shields.io/pypi/l/netlify-python)

This is a partial client library designed to wrap the [Netlify APIs](https://docs.netlify.com/api/get-started/) for python client users.

Full openapi docs: https://open-api.netlify.com/.

This client library is not affiliated with Netlify in any way and provides no guarantees of support or compatibility for Netlify APIs.

## User Guide

This section is intended for developers who want to use the library to make requests to Netlify.

### Installation

⚠ `netlify-python` currently supports python 3.10+.

Recommended installation through [PIP](https://pypi.org/project/netlify-python/) via pypi.

```shell
pip install netlify-python
```

You can also install using [uv](https://docs.astral.sh/uv/):
```shell
uv add netlify-python
```

or [Poetry](https://python-poetry.org/):
```shell
poetry add netlify-python
```

### Usage

This client currently only supports [Personal Access Tokens](https://app.netlify.com/user/applications#personal-access-tokens).  Navigate to User Settings > Applications > Personal Access Tokens and create a new access token.  This is the token you'll use in your initialization of the client.

This created a client that can send http requests.

```python
from netlify import NetlifyClient

client = NetlifyClient(access_token="my-access-token")

client.get_current_user()  # Get current user information
client.create_site_deploy("site-id", "path/to/zip/file.zip")
```

Note that all types are exposed via py.typed so if you are setup with a Pylance server or are using mypy/ty, you can get types automatically from the objects in this library.

### API

This client has minimal support for Netlify APIs based on community need.  The following endpoints are currently supported:
 
| SDK method | API HTTP Method | API Path |
| ---------- | --------------- | -------- |
| `get_current_user()` | `GET` | `/api/v1/user` |
| `create_site(request: CreateSiteRequest)`   | `POST` | `create_site(...)` |
| `list_sites()`         | `GET` | `/api/v1/sites` |
| `get_site(site_id: str)` | `GET` | `/sites/{site_id}` |
| `delete_site(site_id: str)` | `DELETE` | `/api/v1/sites/{site_id}` |
| `create_site_in_team(account_slug: str, request: CreateSiteRequest)` | `POST` |  `/api/v1/{account_slug}/sites` |
| `list_site_files(site_id: str)` |  `GET` |  `/api/v1/sites/{site_id}/files` |
| `get_site_file_by_path_name(site_id: str, file_path: str)` | `GET` | `/api/v1/sites/{site_id}/files/{file_path}` | 
| `create_site_deploy()` | `POST`  | `/api/v1/sites/{site_id}/deploys` |
| `get_site_deploy()` | `GET` | `/api/v1/sites/{site_id}/deploys/{deploy_id}` |


## For Developers

This section is for developers who want to improve this library.  The default development version is on 3.14 but we are currently supporting all python versions >= 3.10.

This library should be developed directly with pip using a venv.

### Development Dependencies

Make sure that you have [`pyenv`](https://github.com/pyenv/pyenv).  You can test this by checking your python version after opening this directory. 
If you need to target a specific version of python you should overwrite your `.python-version` file and ensure you have the specific version installed.

```bash
pyenv install
python --version
```

Make sure your active python version has `virtualenv` setup via:

```bash
python -m pip install virtualenv
```

Create and activate your venv
```bash
python -m venv venv
. venv/bin/activate
```

### Starting development

Everything here out should be executed inside the active venv.

Install your dependencies:
```bash
pip install .[dev]
```

Setup pre-commits:
```bash
pre-commit install
```

You should be good to go now.

### Running tests

Tests are supported via pytest:

```bash
pytest
```

### Building the package
Get your build dependencies in place:

```bash
pip install .[build]
```

Then build the package:
```bash
python -m build
```
