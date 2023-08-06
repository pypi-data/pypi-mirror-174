## extras

[![PyPI](https://img.shields.io/pypi/v/package-extras)](https://pypi.org/project/package-extras/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/package-extras)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)

Package that allows to make assertions about [extras](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras) being installed or not.

For the detailed explanation read [this blog post](https://bmwlog.pp.ua/deprecation-of-package-extras/).

### Usage

For the `pyproject.toml` users

```toml
[tool.poetry.dependencies]
package-extras = { version = "^0.2.0", optional = true }
# your actual extras below
psycopg2 = { version = "^2.9", optional = true }
mysqlclient = { version = "^1.3", optional = true }

[tool.poetry.extras]
databases = ["package-extras", "mysqlclient", "psycopg2"]
```

`setup.py` equivalent

```python
extras_require = \
{'databases': ['package-extras>=0.2.0',
               'psycopg2>=2.9,<3.0',
               'mysqlclient>=1.3,<2.0']}

setup_kwargs = {
    # ... rest of the arguments
    'extras_require': extras_require,
}
setup(**setup_kwargs)
```

Add this or similar block to your code (likely top-level `__init__.py` file)

```python
import warnings

try:
    import package_extras
except ModuleNotFoundError:
    pass
else:
    warnings.warn(
        "'test_package[databases]' extra is deprecated "
        "and will be removed in a future release.",
        category=DeprecationWarning,
        stacklevel=2,
    )
```

Or in case you want to assert the opposite (make sure that extras have been installed)

```python
import warnings

try:
    import package_extras
except ModuleNotFoundError:
    warnings.warn(
        "You are going to use functionality that depends on 'databases' extras. "
        "Please install 'test_package[databases]' to proceed.",
        category=ImportWarning,
        stacklevel=2,
    )
```

> NOTE: `ImportWarning` is ignored by default, so you either need to run `python -W all` or use `RuntimeWarning` instead.

After installation via `pip install test_package[databases]` your package users will get this warning.

```console
>>> import test_package
DeprecationWarning: 'test_package[databases]' extra is deprecated and will be removed in a future release.
```

### Development

```bash
$ poetry install
$ poetry build

$ poetry config pypi-token.pypi my-token
$ poetry publish
```
