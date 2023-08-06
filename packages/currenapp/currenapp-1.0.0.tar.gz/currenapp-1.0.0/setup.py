# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['currenapp']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['currenapp = currenapp.main:app']}

setup_kwargs = {
    'name': 'currenapp',
    'version': '1.0.0',
    'description': 'A CLI to convert different currencies.',
    'long_description': "# Currency Converter CLI\n\n## A Command Line Interface made with Python that convertes different currencies from all the world.\n\n[![GitHub issues](https://img.shields.io/github/issues/caio-bernardo/currencyconv-cli?style=for-the-badge)](https://github.com/caio-bernardo/currencyconv-cli/issues)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n[![GitHub license](https://img.shields.io/github/license/caio-bernardo/currencyconv-cli?color=red&style=for-the-badge)](https://github.com/caio-bernardo/currencyconv-cli/blob/master/LICENSE.md)\n![](https://img.shields.io/badge/STATUS-IN%20PROGRESS-blueviolet?style=for-the-badge)\n\nThis is a small project using [Typer](https://github.com/tiangolo/typer) focusing in learning. The application takes an argument and two optional parameters, the base currency and the target currency, the default is 'BRL' (Brazilian Real) and 'USD' (US Dolar) in that order. After that, the program makes a request to [ExchangeRate-API](https://www.exchangerate-api.com/), which responds with the calculated conversion.\n\n# Table of Contents\n\n[Know Issues](#know-issues) - [Instalation](#instalation) - [Making changes](#making-changes) - [Contributing](#contributing) - [License](#license)\n\n## Know Issues\n\n- ExchangeRate-API imposes a monthly quota of 1500 requests, limiting the usage of the application. Unfortanately, this can't be fixed.\n\n## Instalation\n\nPip Instalation\n```zsh\npip install currenapp\n```\nGo to [[https://www.exchangerate-api.com/]] and Get a Free Key, once you have your key set it on your machine\n``` zsh\nexport EXCHANGERATE_KEY='YOUR KEY'\n```\nAnd it's done. You are free to use the application.\n\n## Making changes\n\nIf you want to make changes to this project you need to clone this repository and have poetry installed.\nAfter cloning, go to the project's directory and initialize the poetry, don't forget to install the dependencies.\n\n```bash\npoetry install\n```\n\nCreate and set your api key in [[https://www.exchangerate-api.com/]] as in [Instalation](#Instalation).\n\nTo run the project use `poetry run python currenapp/main.py` or start the poetry shell to skip these commands.\n\n```zsh\npoetry shell\npython currenapp/main.py\n```\n\n## Contributing\n\nIssues and Pull Request are welcomed. If you want to make suggestions, ask or discuss anything, open a issue.\n\n## License\n\n[MIT](./LICENSE.md)\n",
    'author': 'caio',
    'author_email': 'caio.2004vb@gmail.com',
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
