# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfu_torchac']

package_data = \
{'': ['*'], 'sfu_torchac': ['backend/*']}

install_requires = \
['torch>=1,<2']

setup_kwargs = {
    'name': 'sfu-torchac',
    'version': '0.0.2',
    'description': 'Fast arithmetic coding for PyTorch.',
    'long_description': 'None',
    'author': 'Anderson de Andrade',
    'author_email': 'anderson_de_andrade@sfu.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.12',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
