# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_extras']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'package-extras',
    'version': '0.3.0',
    'description': 'Dummy package to mark extras installation',
    'long_description': '## extras\n\n[![PyPI](https://img.shields.io/pypi/v/package-extras)](https://pypi.org/project/package-extras/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/package-extras)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)\n\nPackage that allows to make assertions about [extras](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras) being installed or not.\n\nFor the detailed explanation read [this blog post](https://bmwlog.pp.ua/deprecation-of-package-extras/).\n\n### Usage\n\nFor the `pyproject.toml` users\n\n```toml\n[tool.poetry.dependencies]\npackage-extras = { version = "^0.2.0", optional = true }\n# your actual extras below\npsycopg2 = { version = "^2.9", optional = true }\nmysqlclient = { version = "^1.3", optional = true }\n\n[tool.poetry.extras]\ndatabases = ["package-extras", "mysqlclient", "psycopg2"]\n```\n\n`setup.py` equivalent\n\n```python\nextras_require = \\\n{\'databases\': [\'package-extras>=0.2.0\',\n               \'psycopg2>=2.9,<3.0\',\n               \'mysqlclient>=1.3,<2.0\']}\n\nsetup_kwargs = {\n    # ... rest of the arguments\n    \'extras_require\': extras_require,\n}\nsetup(**setup_kwargs)\n```\n\nAdd this or similar block to your code (likely top-level `__init__.py` file)\n\n```python\nimport warnings\n\ntry:\n    import package_extras\nexcept ModuleNotFoundError:\n    pass\nelse:\n    warnings.warn(\n        "\'test_package[databases]\' extra is deprecated "\n        "and will be removed in a future release.",\n        category=DeprecationWarning,\n        stacklevel=2,\n    )\n```\n\nOr in case you want to assert the opposite (make sure that extras have been installed)\n\n```python\nimport warnings\n\ntry:\n    import package_extras\nexcept ModuleNotFoundError:\n    warnings.warn(\n        "You are going to use functionality that depends on \'databases\' extras. "\n        "Please install \'test_package[databases]\' to proceed.",\n        category=ImportWarning,\n        stacklevel=2,\n    )\n```\n\n> NOTE: `ImportWarning` is ignored by default, so you either need to run `python -W all` or use `RuntimeWarning` instead.\n\nAfter installation via `pip install test_package[databases]` your package users will get this warning.\n\n```console\n>>> import test_package\nDeprecationWarning: \'test_package[databases]\' extra is deprecated and will be removed in a future release.\n```\n\n### Development\n\n```bash\n$ poetry install\n$ poetry build\n\n$ poetry config pypi-token.pypi my-token\n$ poetry publish\n```\n',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
