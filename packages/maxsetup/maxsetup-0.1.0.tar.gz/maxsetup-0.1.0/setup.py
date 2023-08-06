# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxsetup']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyaml>=21.10.1,<22.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0',
 'ujson>=5.5.0,<6.0.0']

setup_kwargs = {
    'name': 'maxsetup',
    'version': '0.1.0',
    'description': '',
    'long_description': "---\nTitle: README.md\nPath: README.md\nAuthor: Max Ludden\nDate: 2019-01-01 00:00:00\nCSS: static/style.css\n...\n\n# MaxSetup README.md\n\n## Purpose\n\nThis is a module that automates the foundation of a new python project.\n\n## Features from Textualize/Rich:\n\n<br />\n\n> - Generates a custom themed Rich `Console`\n> - Installs Rich's Enhanced Tracebacks\n> - Creates a formatted custom Rich `Progress` Bar.\n> - Provides a helper function to allow for rich to easily print gradient text.\n> - Provides a helper function to allow for rich to easily print a gradient text to a panel.\n\n<br />\n\n## Installation\n\n<br />\n\n#### Install from Pip\n\n```Python\npip install maxsetup\n```\n\n<br />\n\n#### Install from Pipx\n\n```Python\npipx install maxsetup\n```\n\n<br />\n\n#### Install from Pipx\n\n```Python\npython add maxsetup\n```\n<br />\n<hr />\n<br />\n\n## Usage\n\n<br />\n\nThe following are available to import from `maxsetup`:\n\n\n> Not Complete, Will be here soon.\n",
    'author': 'Max Ludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
