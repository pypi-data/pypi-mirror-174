# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['callingcardstools',
 'callingcardstools.database_managers',
 'callingcardstools.database_managers.blockify',
 'callingcardstools.database_managers.macs_like',
 'callingcardstools.database_managers.yeast',
 'callingcardstools.entry_points',
 'callingcardstools.resources',
 'callingcardstools.resources.human',
 'callingcardstools.resources.mouse',
 'callingcardstools.resources.yeast']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.30,<0.30.0',
 'SQLAlchemy>=1.4.41,<2.0.0',
 'biopython>=1.79,<2.0',
 'edlib>=1.3.9,<2.0.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'pysam>=0.19.1,<0.20.0',
 'pysqlite3-binary>=0.4.6,<0.5.0',
 'scipy>=1.8.1,<2.0.0']

entry_points = \
{'console_scripts': ['callingcardstools = callingcardstools:__main__.main']}

setup_kwargs = {
    'name': 'callingcardstools',
    'version': '0.0.2',
    'description': 'A collection of objects and functions to work with calling cards sequencing tools',
    'long_description': "# General use\n\nOnce you have bedtools in your path, you can install like so:\n\n```\npip install callingcardstools\n```\n\nTo start using the command line tools, see the help message with:\n\n```\ncallingcardstools --help\n```\n\n# Development Installation\n\n1. install [poetry](https://python-poetry.org/)\n  - I prefer to set the default location of the virtual environment to the \n  project directory. You can set that as a global configuration for your \n  poetry installation like so: `poetry config virtualenvs.in-project true`\n\n2. git clone the repo\n\n3. cd into the repo and issue the command `poetry install`\n\n4. shell into the virtual environment with `poetry shell`\n\n5. build the package with `poetry build`\n\n6. install the callingcardstools packge into your virtual environment \n  `pip install dist/callingcardstools-...`\n  - Note: you could figure out how to use the pip install `-e` flag to \n  have an interactive development environment. I don't think that is compatible \n  with only the `pyproject.toml` file, but if you look it up, you'll find good \n  stackoverflow instructions on how to put a dummy `setup.py` file in to make \n  this possible",
    'author': 'chase mateusiak',
    'author_email': 'chase.mateusiak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cmatkhan.github.io/callingCardsTools/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
