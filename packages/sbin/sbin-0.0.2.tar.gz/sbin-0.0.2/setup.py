# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bin',
 'bin.bin_file',
 'bin.bin_file.dtos',
 'bin.commands',
 'bin.commands.internal',
 'bin.custom_commands',
 'bin.custom_commands.dtos',
 'bin.env',
 'bin.models',
 'bin.process',
 'bin.process.io',
 'bin.requirements',
 'bin.requirements.dtos',
 'bin.up',
 'bin.up.dtos',
 'bin.virtualenv',
 'bin.virtualenv.dtos']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'colorama>=0.4.5,<0.5.0',
 'pydantic>=1.10.1,<2.0.0',
 'semantic-version>=2.10.0,<3.0.0']

entry_points = \
{'console_scripts': ['bin = bin.main:main', 'sbin = bin.main:main']}

setup_kwargs = {
    'name': 'sbin',
    'version': '0.0.2',
    'description': 'Makes your repo setup clean',
    'long_description': '# bin\n\n`bin` is a CLI that helps you make all of your repo setup uniform.\n',
    'author': 'Mazine Mrini',
    'author_email': 'mazmrini@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/mazmrini/bin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
