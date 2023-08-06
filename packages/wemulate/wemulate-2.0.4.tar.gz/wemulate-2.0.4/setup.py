# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wemulate',
 'wemulate.controllers',
 'wemulate.core',
 'wemulate.core.database',
 'wemulate.ext',
 'wemulate.ext.settings',
 'wemulate.ext.utils',
 'wemulate.plugins',
 'wemulate.templates',
 'wemulate.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.3',
 'colorlog==6.6.0',
 'jinja2==3.1.2',
 'netifaces==0.11.0',
 'pyroute2==0.7.1',
 'pyyaml==6.0',
 'rich>=12.5.1,<13.0.0',
 'tcconfig==0.27.1',
 'typer==0.6.1']

entry_points = \
{'console_scripts': ['wemulate = wemulate.main:app']}

setup_kwargs = {
    'name': 'wemulate',
    'version': '2.0.4',
    'description': 'A modern WAN Emulator',
    'long_description': '**A modern WAN Emulator developed by the Institute for Networked Solutions**\n# WEmulate\n\nHave a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.\n\n## Installation\n\n### Requirements\n* At least two network interfaces for ``LAN-A`` and ``LAN-B``\n* A third management interface if you would like to use the api and frontend module\n* Ubuntu installed\n* Root permissions\n\n### Getting Started\nTo install only the WEmulate cli with bash, simply run this command in your terminal of choice:  \n```\nbash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"\n```\nThere are different arguments available in order to enhance the installation experience:\n```\n-h               Prints the help message\n-f               Skip the confirmation prompt during installation\n-i <int1,int2>   List of interfaces which should be used as management interfaces\n-a               Install the api module\n-v               Install the frontend module\n```\nYou can for example install the cli, api and frontend module together with one management interface with the following command:\n```\ncurl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh | bash -s -- -a -v -i ens2 -f\n```\n\n## Usage \n![WEmulate CLI Commands](/docs/img/animation-wemulate-cli.gif)\n\n```bash\n# Add a new connection\n$ wemulate add connection -n connectionname -i LAN-A LAN-B\n\n# Delete a connection\n$ wemulate delete connection -n connectionname\n\n# Add parameters bidirectional\n$ wemulate add parameter -n connectionname -j 20 -d 40\n\n# Add parameters in specific direction\n$ wemulate add parameter -n connectionname -j 20 -d 40 -src LAN-A -dst LAN-B\n\n```\n\n## Development\nConfigure poetry to create the environment inside the project path, in order that VSCode can recognize the virtual environment.\n```\n$ poetry config virtualenvs.in-project true\n```\nInstall the virtualenv.\n```\n$ poetry install\n```\n',
    'author': 'Julian Klaiber',
    'author_email': 'julian.klaiber@ost.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://wemulate.github.io/wemulate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
