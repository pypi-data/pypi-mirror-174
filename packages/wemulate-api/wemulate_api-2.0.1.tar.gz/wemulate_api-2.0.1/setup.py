# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api', 'api.core', 'api.routers', 'api.schemas']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3.1.2',
 'MarkupSafe==2.1.1',
 'Werkzeug==2.1.2',
 'aniso8601==9.0.1',
 'attrs==21.4.0',
 'click==8.1.3',
 'fastapi==0.70.0',
 'itsdangerous==2.1.2',
 'jsonschema==4.7.2',
 'pyrsistent==0.18.1',
 'pytz==2022.1',
 'six==1.16.0',
 'uvicorn==0.15.0',
 'wemulate>=2.0.3,<3.0.0']

entry_points = \
{'console_scripts': ['wemulate-api = api.app:main']}

setup_kwargs = {
    'name': 'wemulate-api',
    'version': '2.0.1',
    'description': 'API for the modern WAN Emulator (WEmulate)',
    'long_description': '**A modern WAN Emulator developed by the Institute for Networked Solutions**\n# WEmulate API Module\nThis is the API module which builds on the [CLI module](https://github.com/wemulate/wemulate).\n\nHave a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.\n\n## Installation\nIt is installed with the `-a` parameter from the documented install command for [WEmulate](https://github.com/wemulate/wemulate).\n\n## Development\nConfigure poetry to create the environment inside the project path, in order that VSCode can recognize the virtual environment.\n```\n$ poetry config virtualenvs.in-project true\n```\nInstall the virtualenv.\n```\n$ poetry install\n```\nStart the application with the following command:\n```\n$ uvicorn api.app:app --host 0.0.0.0 --port 8080 --reload\n```',
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
