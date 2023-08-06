# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdyna']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xdyna',
    'version': '0.0.3',
    'description': 'Xsuite dynamics package',
    'long_description': '# xdyna\nTools to study beam dynamics in xtrack simulations, like dynamic aperture calculations, PYTHIA integration, dynamic indicators, ...\n',
    'author': 'Frederik F. Van der Veken',
    'author_email': 'frederik@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xsuite/xdyna',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
