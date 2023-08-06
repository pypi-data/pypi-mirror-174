# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mypkg7727']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mypkg7727',
    'version': '0.1.0',
    'description': 'A package for doing great things!',
    'long_description': '# mypkg7727\n\nA package for doing great things!\n\n## Installation\n\n```bash\n$ pip install mypkg7727\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`mypkg7727` was created by Monty Python. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`mypkg7727` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Monty Python',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
