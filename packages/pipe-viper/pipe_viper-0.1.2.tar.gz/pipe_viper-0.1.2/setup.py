# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipe_viper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pipe-viper',
    'version': '0.1.2',
    'description': 'Pwsh utils for python',
    'long_description': '# Pipe Viper Plugin\n\n* This core plugin is meant simply for time savings and only uses the standard Python library, the goal is no additional dependencies.\n* Plugins may take dependencies in the future  \n  \n__Currently only supports running a single `.ps1` or `string` Powershell command.__  \nI plan to add support for command scripts and other shells, as well as supporting libraries of useful script functionality. Though, this plugin will be primarily focused on PowerShell related functionality unless someone else expands on other shell support.\n\n## https://pypi.org/project/pipe-viper/',
    'author': 'Josh S Wilkinson',
    'author_email': 'JoshsWilkinson@Outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Phelsong/pipe_viper',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
