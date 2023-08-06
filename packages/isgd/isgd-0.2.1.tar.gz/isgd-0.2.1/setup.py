# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isgd']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'isgd',
    'version': '0.2.1',
    'description': '🔗 A CLI to shorten url(s) using is.gd/v.gd',
    'long_description': '# `isgd`\n\n**Usage**:\n\n```console\nisgd [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n# `isgd`\n\n**Usage**:\n\n```console\n$ isgd [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: create a shortened url using is.gd or v.gd\n* `stats`\n\n## `isgd create`\n\ncreate a shortened url using is.gd or v.gd\n\n**Usage**:\n\n```console\n$ isgd create [OPTIONS] URL\n```\n\n**Arguments**:\n\n* `URL`: [required]\n\n**Options**:\n\n* `--custom-url TEXT`: Customize your url(s)\n* `--log-stat / --no-log-stat`: Track your url(s)  [default: False]\n* `--verify-ssl / --no-verify-ssl`: enable/disable ssl for your url(s)  [default: True]\n* `--vgd / --no-vgd`: use v.gd domain for your url(s)  [default: False]\n* `--help`: Show this message and exit.\n\n## `isgd stats`\n\n**Usage**:\n\n```console\n$ isgd stats [OPTIONS] URL\n```\n\n**Arguments**:\n\n* `URL`: [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n* `create`: create a shortened url using is.gd or v.gd\n* `stats`\n\n## `isgd create`\n\ncreate a shortened url using is.gd or v.gd\n\n**Usage**:\n\n```console\nisgd create [OPTIONS] URL\n```\n\n**Arguments**:\n\n* `URL`: [required]\n\n**Options**:\n\n* `--custom-url TEXT`: Customize your url(s)\n* `--log-stat / --no-log-stat`: Track your url(s)  [default: False]\n* `--verify-ssl / --no-verify-ssl`: enable/disable ssl for your url(s)  [default: True]\n* `--vgd / --no-vgd`: use v.gd domain for your url(s)  [default: False]\n* `--help`: Show this message and exit.\n\n## `isgd stats`\n\n**Usage**:\n\n```console\nisgd stats [OPTIONS] URL\n```\n\n**Arguments**:\n\n* `URL`: [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'nitr7gen',
    'author_email': 'nitr7gen@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
