# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcoll', 'xcoll.beam_elements', 'xcoll.scattering_routines.k2']

package_data = \
{'': ['*'],
 'xcoll.beam_elements': ['collimators_src/*'],
 'xcoll.scattering_routines.k2': ['FORTRAN_src/*',
                                  'FORTRAN_src/crlibm/*',
                                  'FORTRAN_src/roundctl/*']}

setup_kwargs = {
    'name': 'xcoll',
    'version': '0.1.2',
    'description': 'Xsuite collimation package',
    'long_description': '# xcoll\n\n<!---![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xcoll?logo=PyPI?style=plastic) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/xcoll?logo=PyPI?style=plastic)-->\n\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/xsuite/xcoll?style=plastic) ![GitHub](https://img.shields.io/github/license/xsuite/xcoll?style=plastic) ![GitHub all releases](https://img.shields.io/github/downloads/xsuite/xcoll/total?logo=GitHub&style=plastic) ![GitHub issues](https://img.shields.io/github/issues/xsuite/xcoll?logo=GitHub&style=plastic) ![GitHub pull requests](https://img.shields.io/github/issues-pr/xsuite/xcoll?logo=GitHub&style=plastic) ![GitHub repo size](https://img.shields.io/github/repo-size/xsuite/xcoll?logo=GitHub&style=plastic)\n\nCollimation in xtrack simulations\n\n## Description\n\n## Getting Started\n\n### Dependencies\n\n* python >= 3.8\n    * numpy\n    * pandas\n    * xsuite (in particular xobjects, xdeps, xtrack, xpart)\n* to use K2:\n    * gfortran \n\n### Installing\n`xcoll` is packaged using `poetry`, and can be easily installed with `pip`:\n```bash\npip install xcoll\n```\nFor a local installation, clone and install in editable mode (need to have `pip` >22):\n```bash\ngit clone git@github.com:xsuite/xcoll.git\npip install -e xcoll\n```\n\n### Using K2\nTo be able to use the K2 scattering algorithms, these need to be compiled from source.\nThere is a small script that does this (you can ignore the warnings):\n```bash\ncd xcoll\n./compile_K2.sh\n```\nThis installs a shared library in the package that is tailored to your current python installation.\n\nWithout compilation, K2 Collimators can be installed in a `Line`, but not tracked.\n\n### Example\n\n## Features\n\n## Authors\n\n* [Frederik Van der Veken](https://github.com/freddieknets) (frederik@cern.ch)\n* [Despina Demetriadou](https://github.com/ddemetriadou)\n* [Andrey Abramov](https://github.com/anabramo)\n* [Giovanni Iadarola](https://github.com/giadarol)\n\n\n## Version History\n\n* 0.1\n    * Initial Release\n\n## License\n\nThis project is [Apache 2.0 licensed](./LICENSE).\n',
    'author': 'Frederik F. Van der Veken',
    'author_email': 'frederik@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xsuite/xcoll',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
