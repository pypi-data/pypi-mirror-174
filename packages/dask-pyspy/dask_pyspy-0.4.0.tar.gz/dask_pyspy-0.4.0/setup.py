# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dask_pyspy']

package_data = \
{'': ['*']}

install_requires = \
['distributed>=2.30.0', 'py-spy>=0.3.9,<0.4.0']

setup_kwargs = {
    'name': 'dask-pyspy',
    'version': '0.4.0',
    'description': 'Profile dask distributed clusters with py-spy',
    'long_description': 'None',
    'author': 'Gabe Joseph',
    'author_email': 'gjoseph92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
