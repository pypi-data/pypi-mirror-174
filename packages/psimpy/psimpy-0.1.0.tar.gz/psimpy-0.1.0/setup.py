# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psimpy',
 'psimpy.emulator',
 'psimpy.inference',
 'psimpy.sampler',
 'psimpy.sensitivity',
 'psimpy.simulator',
 'psimpy.utility']

package_data = \
{'': ['*']}

install_requires = \
['SALib>=1.4.5,<2.0.0',
 'beartype>=0.11.0,<0.12.0',
 'numpy>=1.22.3,<2.0.0',
 'rpy2>=3.5.1,<4.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'psimpy',
    'version': '0.1.0',
    'description': 'Predictive and probabilistic simulation tools.',
    'long_description': '## Description\n\n`PSimPy` (Predictive and probabilistic simulation with Python) implements\na Gaussian process emulation-based framework that enables systematically and\nefficiently inverstigating uncertainties associated with physics-based models\n(i.e. simulators).\n\n## Installation\n\nTo be input soon...\n\n## Usage\n\n## License\n\n`PSimPy` was created by Hu Zhao at the Chair of Methods for Model-based\nDevelopment in Computational Engineering. It is licensed under the terms of\nthe MIT license.',
    'author': 'Hu Zhao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
