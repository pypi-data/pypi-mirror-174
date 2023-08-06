# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memfault_cli']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7,<9',
 'mflt-build-id==0.0.5',
 'more_itertools>=8.0.2,<9.0.0',
 'pyaxmlparser>=0.3.24,<0.4.0',
 'pyelftools>=0.26,<=0.28',
 'requests>=2.22.0,<3.0.0',
 'tqdm>=4.44.1,<5.0.0',
 'urllib3>=1.26.7']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata==4.8.3']}

entry_points = \
{'console_scripts': ['memfault = memfault_cli.cli:main']}

setup_kwargs = {
    'name': 'memfault-cli',
    'version': '0.13.0',
    'description': 'Memfault CLI tool',
    'long_description': '# Memfault CLI tool\n\nThis package contains the `memfault` CLI tool.\n\nThe purpose of the tool is to make integration with Memfault from other systems,\nlike continuous integration servers, as easy as possible.\n\nInstall the tool and run `memfault --help` for more info!\n',
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://docs.memfault.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
