# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrfume', 'pyrfume.loaders', 'pyrfume.unit_test']

package_data = \
{'': ['*']}

install_requires = \
['PubChemPy>=1.0.4,<2.0.0',
 'datajoint<0.13.5',
 'eden-kernel>=0.3.1348,<0.4.0',
 'ipykernel>=5.5.6,<6.15.1',
 'mordred>=1.2.0,<2.0.0',
 'numpy<1.20.3',
 'pandas>1.0.5',
 'plotly>=5.9.0,<6.0.0',
 'quantities>=0.13.0,<0.14.0',
 'rdkit-pypi>=2022.3.4,<2023.0.0',
 'requests>=2.20.0,<=2.27.1',
 'scikit-learn>=0.23.1,<=0.24.2',
 'scipy>=1.4.1,<=1.5.4',
 'sympy>=1.6,<=1.9',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{'optimize': ['deap>=1.3.1,<2.0.0', 'dask[bag]<=2021.3.0']}

setup_kwargs = {
    'name': 'pyrfume',
    'version': '0.18.2',
    'description': 'A validation library for human olfactory psychophysics research.',
    'long_description': '# Pyrfume\n\n![Pyrfume logo](https://avatars3.githubusercontent.com/u/34174393?s=200&v=4)\n\n#### `pyrfume` is a python library for olfactory psychophysics research. See "notebooks" for examples of use.\n[![Python package](https://github.com/pyrfume/pyrfume/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/pyrfume/pyrfume/actions/workflows/pythonpackage.yml)\n[![Travis](https://travis-ci.org/pyrfume/pyrfume.svg?branch=master)](https://travis-ci.org/pyrfume/pyrfume) \n[![Coverage Status](https://coveralls.io/repos/github/pyrfume/pyrfume/badge.svg?branch=master)](https://coveralls.io/github/pyrfume/pyrfume?branch=master)\n![Zenodo](https://user-images.githubusercontent.com/549787/165869234-79bf95db-0b6c-495c-a1a8-b3db751f3352.png)\n\n\n### Examples:\n```\n# Load data for Snitz et al, 2013 (PLOS Computational Biology)\nimport pyrfume\nbehavior = pyrfume.load_data(\'snitz_2013/behavior.csv\')\nmolecules = pyrfume.load_data(\'snitz_2013/molecules.csv\')\n\n# Load data for Bushdid et al, 2014 (Science)\nimport pyrfume\nbehavior = pyrfume.load_data(\'bushdid_2014/behavior.csv\')\nmolecules = pyrfume.load_data(\'bushdid_2014/molecules.csv\')\nmixtures = pyrfume.load_data(\'bushdid_2014/behavior.csv\')\n```\n\n### Contributing\n\nJust run `./develop.sh` to get started with developing `pyrfume`.\n\n### [Website](http://pyrfume.org)\n\n### [Data Repository](https://github.com/pyrfume/pyrfume-data)\n\n### [Data Curation Status](http://status.pyrfume.org)\n\n### [Docs](https://pyrfume.readthedocs.io/)\n\n*Licensing/Copyright*: Data is provided as-is.  Licensing information for individual datasets is available in the data repository.  Takedown requests for datasets may be directed to admin at pyrfume dot org.  \n',
    'author': 'Rick Gerkin',
    'author_email': 'rgerkin@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://pyrfume.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
