# Netlify Python Client

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netlify-python)

This is a work in progress package designed to wrap the [Netlify APIs](https://docs.netlify.com/api/get-started/) for python client users.

Note that this library is still very unstable and not yet ready for general use.

## Developer Setup

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