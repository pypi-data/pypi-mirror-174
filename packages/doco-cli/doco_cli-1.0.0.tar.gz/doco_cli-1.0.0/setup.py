# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.commands',
 'src.commands.backups',
 'src.commands.backups.raw',
 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['doco = src.main:app']}

setup_kwargs = {
    'name': 'doco-cli',
    'version': '1.0.0',
    'description': '',
    'long_description': '# Doco CLI\n\n**doco** (**do**cker **co**mpose tool) is a command line tool\nfor working with [Docker Compose](https://docs.docker.com/compose/compose-file/) projects\n(pretty-printing status, creating backups using rsync, batch commands and more).\n\n[![Code style](https://github.com/bibermann/doco-cli/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/bibermann/doco-cli/actions/workflows/pre-commit.yml)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![PyPI](https://img.shields.io/pypi/v/doco-cli)](https://pypi.org/project/doco-cli)\n\n## Usage\n\nExample calls:\n\n- `doco s *`: Print pretty status of all _docker compose_ projects in the current directory.\n- `doco s . -aa`: Print most detailled status of a _docker compose_ project (including variables and volumes).\n- `doco r .`: Equivalent of `docker compose down --remove-orphans && docker compose up --build -d`.\n- `doco backups create . --dry-run`: See what would be done to create a backup of a _docker compose_ project.\n\nTo explore all possibilities, run `doco -h` or see  [docs/doco-help.md](docs/doco-help.md).\n\n## Installation\n\n```bash\npipx install doco-cli\ndoco --install-completion\n```\n\nOr install from source, see [docs/installation.md](docs/installation.md).\n\n## Configuration\n\nTo create a backup, you need to create a `doco.config.json` file.\n\nSee [docs/configuration.md](docs/configuration.md).\n\n## Development\n\nTo start developing, see [docs/development.md](docs/development.md).\n',
    'author': 'Fabian Sandoval Saldias',
    'author_email': 'fabianvss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bibermann/doco-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
