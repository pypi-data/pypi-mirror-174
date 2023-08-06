# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haptools', 'haptools.data']

package_data = \
{'': ['*']}

install_requires = \
['brewer2mpl>=1.4.1',
 'click>=8.0.3',
 'cyvcf2>=0.30.14',
 'matplotlib>=3.5.1',
 'pysam>=0.19.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2',
          'sphinx-autodoc-typehints>=1.12.0',
          'sphinx-rtd-theme>=1.0.0',
          'numpydoc>=1.1.0',
          'sphinx-click>=3.0.2'],
 'files': ['Pgenlib>=0.81.2']}

entry_points = \
{'console_scripts': ['haptools = haptools.__main__:main']}

setup_kwargs = {
    'name': 'haptools',
    'version': '0.0.1',
    'description': 'Simulate genotypes and phenotypes for GWAS and subsequent fine-mapping',
    'long_description': None,
    'author': 'Michael Lamkin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cast-genomics/haptools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
