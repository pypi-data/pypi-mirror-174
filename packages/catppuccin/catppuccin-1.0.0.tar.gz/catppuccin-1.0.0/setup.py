# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['catppuccin']
setup_kwargs = {
    'name': 'catppuccin',
    'version': '1.0.0',
    'description': '🐍 Soothing pastel theme for Python.',
    'long_description': '<h3 align="center">\n\t<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>\n\t<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>\n\tCatppuccin for <a href="https://www.python.org/">Python</a>\n\t<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>\n</h3>\n\n<p align="center">\n\t<a href="https://github.com/catppuccin/python/stargazers"><img src="https://img.shields.io/github/stars/catppuccin/python?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>\n\t<a href="https://github.com/catppuccin/python/issues"><img src="https://img.shields.io/github/issues/catppuccin/python?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>\n\t<a href="https://github.com/catppuccin/python/contributors"><img src="https://img.shields.io/github/contributors/catppuccin/python?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>\n</p>\n\n## Installation\n\nInstall with `pip` or your preferred dependency management tool.\n\n```bash\npip install catppuccin\n```\n\n## Usage\n\n```python\n>>> from catppuccin import Flavour\n>>> Flavour.latte().mauve.hex\n\'8839ef\'\n>>> Flavour.mocha().teal.rgb\n(148, 226, 213)\n```\n\n`Flavour` is a [`dataclass`](https://docs.python.org/3/library/dataclasses.html),\nso you can inspect its fields to get access to the full set of colour names and values:\n\n```python\n>>> from dataclasses import fields\n>>> flavour = Flavour.frappe()\n>>> for field in fields(flavour):\n        colour = getattr(flavour, field.name)\n        print(f"{field.name}: #{colour.hex}")\nrosewater: #f2d5cf\nflamingo: #eebebe\npink: #f4b8e4\n...\nbase: #303446\nmantle: #292c3c\ncrust: #232634\n```\n\n## Contribution\n\nIf you are looking to contribute, please read through our\n[CONTRIBUTING.md](https://github.com/catppuccin/.github/blob/main/CONTRIBUTING.md)\nfirst!\n\n### Development\n\nThis project is maintained with [Poetry](https://python-poetry.org). If you\ndon\'t have Poetry yet, you can install it using the [installation\ninstructions](https://python-poetry.org/docs/#installation).\n\nInstall the project\'s dependencies:\n\n```bash\npoetry install\n```\n\n#### Code Standards\n\nBefore committing changes, it is recommended to run the following tools to\nensure consistency in the codebase.\n\n```bash\nisort .\nblack .\npylint catppuccin.py\nmypy .\npytest --cov\n```\n\nThese tools are all installed as part of the `dev` dependency group with\nPoetry. You can use `poetry shell` to automatically put these tools in your\npath.\n\n\n## 💝 Thanks to\n\n-   [backwardspy](https://github.com/backwardspy)\n\n&nbsp;\n\n<p align="center">\n\t<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" />\n</p>\n<p align="center">\n\tCopyright &copy; 2022-present <a href="https://github.com/catppuccin" target="_blank">Catppuccin Org</a>\n</p>\n<p align="center">\n\t<a href="https://github.com/catppuccin/catppuccin/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>\n</p>\n',
    'author': 'backwardspy',
    'author_email': 'backwardspy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
