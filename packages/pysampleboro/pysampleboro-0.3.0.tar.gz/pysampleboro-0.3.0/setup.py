# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysampleboro']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0']

extras_require = \
{'docs': ['Sphinx>=5.0,<6.0',
          'sphinx-rtd-theme>=1.0,<2.0',
          'myst-parser>=0.18,<0.19']}

setup_kwargs = {
    'name': 'pysampleboro',
    'version': '0.3.0',
    'description': 'My Python package to help you get up to speed.',
    'long_description': '# pysampleboro\n\n<p align="center">\n  <a href="https://github.com/alborotogarcia/pysampleboro/actions?query=workflow%3ACI">\n    <img src="https://img.shields.io/github/workflow/status/alborotogarcia/pysampleboro/CI/master?label=CI&logo=github&style=flat-square" alt="CI Status" >\n  </a>\n  <a href="https://pysampleboro.readthedocs.io">\n    <img src="https://img.shields.io/readthedocs/pysampleboro.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">\n  </a>\n  <a href="https://codecov.io/gh/alborotogarcia/pysampleboro">\n    <img src="https://img.shields.io/codecov/c/github/alborotogarcia/pysampleboro.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">\n  </a>\n</p>\n<p align="center">\n  <a href="https://python-poetry.org/">\n    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">\n  </a>\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">\n  </a>\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">\n  </a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/pysampleboro/">\n    <img src="https://img.shields.io/pypi/v/pysampleboro.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">\n  </a>\n  <img src="https://img.shields.io/pypi/pyversions/pysampleboro.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">\n  <img src="https://img.shields.io/pypi/l/pysampleboro.svg?style=flat-square" alt="License">\n</p>\n\nMy Python package to help you get up to speed.\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install pysampleboro`\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- prettier-ignore-start -->\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tbody>\n    <tr>\n      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alborotogarcia"><img src="https://avatars.githubusercontent.com/u/59288789?v=4?s=80" width="80px;" alt="alborotogarcia"/><br /><sub><b>alborotogarcia</b></sub></a><br /><a href="https://github.com/alborotogarcia/pysampleboro/commits?author=alborotogarcia" title="Code">💻</a> <a href="#ideas-alborotogarcia" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alborotogarcia/pysampleboro/commits?author=alborotogarcia" title="Documentation">📖</a></td>\n    </tr>\n  </tbody>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n<!-- prettier-ignore-end -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)\nproject template.\n',
    'author': 'Alvaro Gallego',
    'author_email': 'agallego@achlys.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alborotogarcia/pysampleboro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
