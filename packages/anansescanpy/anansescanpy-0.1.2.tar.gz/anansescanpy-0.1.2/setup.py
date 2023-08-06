# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anansescanpy']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.8.0,<0.9.0',
 'jupyterlab>=3.3.4,<4.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'scanpy>=1.9.1,<2.0.0',
 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'anansescanpy',
    'version': '0.1.2',
    'description': 'implementation of scANANSE for scanpy objects in Python',
    'long_description': '# AnanseScanpy\nImplementation of scANANSE for Scanpy objects in Python\n\n# Getting started\n\n## Installation\n\nThe most straightforward way to install AnanseScanpy is via conda using pypi.\n\n### Install package through Conda\nIf you have not used Bioconda before, first set up the necessary channels (in this order!). \nYou only have to do this once.\n```\n$ conda config --add channels defaults\n$ conda config --add channels bioconda\n$ conda config --add channels conda-forge\n```\n\nThen install AnanseScanpy with:\n```\n$ conda install anansescanpy\n```\n\n### Install package through PyPI\n```\n$ pip install anansescanpy\n```\n\n### Install package through GitHub\n```\ngit clone https://github.com/Arts-of-coding/AnanseScanpy.git\ncd AnanseScanpy\nconda env create -f requirements.yaml\nconda activate AnanseScanpy\npip install -e .\n```\n\n## Start using the package\n\n### Run the package either in the console\n```\n$ python3\n```\n\n### Or run the package in jupyter notebook\n```\n$ jupyter notebook\n```\n\n## For extended documentation see our ipynb vignette\nTODO\n',
    'author': 'J Arts (Arts-of-coding)',
    'author_email': 'julian.armando.arts@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Arts-of-coding/AnanseScanpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
