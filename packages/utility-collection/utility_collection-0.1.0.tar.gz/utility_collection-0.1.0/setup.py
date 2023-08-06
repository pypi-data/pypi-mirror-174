# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utility_collection',
 'utility_collection.common',
 'utility_collection.download_file_samples']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'requests>=2.28.1,<3.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['build = utility_collection.build:run']}

setup_kwargs = {
    'name': 'utility-collection',
    'version': '0.1.0',
    'description': '',
    'long_description': '# utility-collection\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
