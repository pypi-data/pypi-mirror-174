# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_dev_deps']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.0,<6.0',
 'autopep8>=2.0,<3.0',
 'black>=22.0,<23.0',
 'doc8',
 'flake8>=5.0,<6.0',
 'ipdb',
 'isort>=5.0,<6.0',
 'm2r2',
 'mdformat_myst',
 'mypy',
 'pipdeptree>=2.0,<3.0',
 'pre-commit>=2.0,<3.0',
 'pylint>=2.0,<3.0',
 'pytest-asyncio',
 'pytest-benchmark>=4.0,<5.0',
 'pytest-cov>=4.0,<5.0',
 'pytest-datadir>=1.0,<2.0',
 'pytest-datafiles>=2.0,<3.0',
 'pytest-freezegun',
 'pytest-mock>=3.0,<4.0',
 'pytest-pep8>=1.0,<2.0',
 'pytest-profiling>=1.0,<2.0',
 'pytest-randomly>=3.0,<4.0',
 'pytest-vcr>=1.0,<2.0',
 'pytest-voluptuous>=1.0,<2.0',
 'pytest-xdist>=3.0,<4.0',
 'pytest>=7.0,<8.0',
 'readme-renderer[md]>=37.0,<38.0',
 'requests-mock>=1.0,<2.0',
 'setuptools',
 'sphinx-autoapi>=2.0,<3.0',
 'sphinx-autodoc-typehints>=1.0,<2.0',
 'sphinx-rtd-theme>=1.0,<2.0',
 'tox',
 'twine>=4.0,<5.0',
 'wheel']

setup_kwargs = {
    'name': 'py-dev-deps',
    'version': '0.5.0',
    'description': 'A package for common python development dependencies',
    'long_description': "# py-dev-deps\n\nA project that only manages python development dependencies\n\nThe aim of this project is to provide a common denominator for python development dependencies\nin one package that can be added as a development dependency to other projects.  By using\npoetry to resolve and maintain a common set of compatible development dependencies, it may\nhelp to reduce the burdens of package installations for projects using this project as a\ndevelopment dependency.\n\n## Install\n\nSee [INSTALL](INSTALL.md) for more details; the following should work; note that\nthe intention is to use this package only for development dependencies.\n\n#### poetry\n\n```sh\npoetry add -D 'py-dev-deps'\n```\n\n#### pip\n\n```sh\ncat >> dev-requirements.txt <<EOF\npy-dev-deps\nEOF\n\npip install -r dev-requirements.txt\n```\n",
    'author': 'Darren Weber',
    'author_email': 'dweber.consulting@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dazza-codes/py-dev-deps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
