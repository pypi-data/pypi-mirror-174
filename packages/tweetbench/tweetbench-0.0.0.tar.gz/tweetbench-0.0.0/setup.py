# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tweetbench']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['tweetbench = tweetbench.__main__:main']}

setup_kwargs = {
    'name': 'tweetbench',
    'version': '0.0.0',
    'description': 'tweetbench',
    'long_description': "# tweetbench\n\n[![PyPI](https://img.shields.io/pypi/v/tweetbench.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/tweetbench.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/tweetbench)][python version]\n[![License](https://img.shields.io/pypi/l/tweetbench)][license]\n\n[![Read the documentation at https://tweetbench.readthedocs.io/](https://img.shields.io/readthedocs/tweetbench/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/freddyheppell/tweetbench/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/freddyheppell/tweetbench/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/tweetbench/\n[status]: https://pypi.org/project/tweetbench/\n[python version]: https://pypi.org/project/tweetbench\n[read the docs]: https://tweetbench.readthedocs.io/\n[tests]: https://github.com/freddyheppell/tweetbench/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/freddyheppell/tweetbench\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _tweetbench_ via [pip] from [PyPI]:\n\n```console\n$ pip install tweetbench\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license],\n_tweetbench_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/freddyheppell/tweetbench/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/freddyheppell/tweetbench/blob/main/LICENSE\n[contributor guide]: https://github.com/freddyheppell/tweetbench/blob/main/CONTRIBUTING.md\n[command-line reference]: https://tweetbench.readthedocs.io/en/latest/usage.html\n",
    'author': 'Freddy Heppell',
    'author_email': 'freddy@freddyheppell.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/freddyheppell/tweetbench',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
