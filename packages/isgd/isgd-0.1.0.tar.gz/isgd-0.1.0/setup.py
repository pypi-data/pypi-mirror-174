# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isgd']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['isgd = isgd.main:app']}

setup_kwargs = {
    'name': 'isgd',
    'version': '0.1.0',
    'description': '',
    'long_description': '# isgd\n\n> readme coming soon...\n',
    'author': 'nitr7gen',
    'author_email': 'nitr7gen@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
