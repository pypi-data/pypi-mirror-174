# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flask_vite', 'tests']

package_data = \
{'': ['*'], 'flask_vite': ['starter/*', 'starter/src/*']}

install_requires = \
['Flask>=2,<3', 'rich>=12.5.1,<13.0.0']

entry_points = \
{'flask.commands': ['vite = flask_vite.cli:vite']}

setup_kwargs = {
    'name': 'flask-vite',
    'version': '0.1.6',
    'description': 'Flask+Vite integration.',
    'long_description': "# Flask-Vite\n\n[![image](https://img.shields.io/pypi/v/flask-tailwind.svg)](https://pypi.python.org/pypi/flask-tailwind)\n\nPlugin to simplify use of Vite from Flask.\n\n-   Status: Alpha.\n-   Free software: MIT license\n\n## Usage\n\nInstantiate the Flask extension as you do for other Flask extensions:\n\n```python\nfrom flask_vite import Vite\n\napp = Flask(...)\nvite = Vite(app)\n\n# or\nvite = Vite()\nvite.init_app(app)\n```\n\nThen you can use the following commands:\n\n```text\n$ flask vite\nUsage: flask vite [OPTIONS] COMMAND [ARGS]...\n\nPerform Vite operations.\n\nOptions:\n--help  Show this message and exit.\n\nCommands:\nbuild          Build the Vite assets.\ncheck-updates  Check outdated Vite dependencies.\ninit           Init the vite/ directory (if it doesn't exist)\ninstall        Install the dependencies using npm.\nstart          Start watching source changes for dev.\nupdate         Update Vite and its dependencies, if needed.\n```\n\n## Features\n\n- Manages a `vite` directory where you put your front-end source code.\n- Auto-injects vite-generated assets into your HTML pages.\n\n## Credits\n\nThis project is inspired by the\n[Django-Tailwind](https://github.com/timonweb/django-tailwind) project.\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter), using the\n[abilian/cookiecutter-abilian-python](https://github.com/abilian/cookiecutter-abilian-python)\nproject template.\n",
    'author': 'Abilian SAS',
    'author_email': 'contact@abilian.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/abilian/flask-vite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
