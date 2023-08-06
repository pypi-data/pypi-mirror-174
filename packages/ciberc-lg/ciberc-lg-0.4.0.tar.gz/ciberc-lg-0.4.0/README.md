# CiberC-LG

Utility SDK to Cimcon Lighting Gale Platform.

## Installation

This lib is intended to be published in PyPi. For developer mode install from source.

```bash
# From pypi
pip install ciberc-lg
# or pipenv

# From source
pip install -r requirements/production.txt
# For dev (optional)
pip install -r requirements/dev.txt
# or use Pipenv
pipenv install --dev
```

## Use

```python
from lg import LGApi, LGAuth

...
lg_auth = LGAuth(username, password, base_url, ssl_verify=False, ...)
lg_api - LGApi(lg_auth)
...
```

## Code documentation

Use sphinx to generate autodoc:

```bash
# Make once
sphinx-quickstart docs
sphinx-build -b html docs/source/ docs/build/html

# update docs
cd docs
make clean html
```

## Tests

Slow tests make request.

```bash
pytest -s
pytest tests/lg/test_x.py::func_name
```

## Build

```bash
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
pip install ciberc-lg

## Test PyPI
twine upload --repository testpypi dist/*
pip install -i https://test.pypi.org/simple/ --no-deps <PACKAGE-NAME>
```

## Versioning

There are varios files that hardcode version. Use edit with replace and search to find all. Be consistent.

Format: 0.0.0

- conf.py
- setup.py
- git tag -a vx.y.z
