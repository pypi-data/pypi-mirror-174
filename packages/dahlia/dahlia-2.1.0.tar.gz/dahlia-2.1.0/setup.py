# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dahlia']

package_data = \
{'': ['*'],
 'dahlia': ['.mypy_cache/*',
            '.mypy_cache/3.10/*',
            '.mypy_cache/3.9/*',
            '.mypy_cache/3.9/_typeshed/*',
            '.mypy_cache/3.9/collections/*',
            '.mypy_cache/3.9/ctypes/*',
            '.mypy_cache/3.9/dahlia/*',
            '.mypy_cache/3.9/email/*',
            '.mypy_cache/3.9/importlib/*',
            '.mypy_cache/3.9/importlib/metadata/*',
            '.mypy_cache/3.9/os/*']}

entry_points = \
{'console_scripts': ['dahlia = dahlia.__main__:main']}

setup_kwargs = {
    'name': 'dahlia',
    'version': '2.1.0',
    'description': 'A library allowing you to use Minecraft format codes in strings.',
    'long_description': '[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dahlia)](https://pypi.python.org/pypi/dahlia)\n[![PyPI version](https://badge.fury.io/py/dahlia.svg)](https://badge.fury.io/py/dahlia)\n[![Documentation Status](https://readthedocs.org/projects/dahlia/badge/?version=latest)](https://dahlia.readthedocs.io/en/latest/?badge=latest)\n# Dahlia\n\nDahlia is a simple text formatting package, inspired by text formatting in the game Minecraft.\n\nText is formatted in a similar way to in the game. With Dahlia, it is formatted by typing a special character `&` followed by a format code and finally the text to be formatted.\n\n## Installation\n\nDahlia is available on PyPI and can be installed with pip, or any other Python package manager:\n\n```\n$ pip install dahlia\n```\n(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead)\n\n## Documentation\n\nDahlia documentation is available at https://dahlia.readthedocs.io.\n\n## License\n\nDahlia is licensed under the MIT License.\n\n## Examples\n\n<img width="805" alt="Screen Shot 2022-10-05 at 22 56 57" src="https://user-images.githubusercontent.com/77130613/194162110-fb77713c-7008-4f5f-a79c-7a3666f2fd11.png">\n',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trag1c/Dahlia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
