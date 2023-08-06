# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strike_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'strike-api',
    'version': '0.1.3',
    'description': 'A python client for the strike api',
    'long_description': '# strike-python\nA python client for the https://strike.me API.  \n\n## Example Usage\n`$ export STRIKE_API_KEY=<STRIKE_API_KEY>`\n```python\nfrom strike_api import rates\n\nrates = rates.get_ticker()\n```\n\n## Build strike-api\n[Install Poetry](https://python-poetry.org/docs/#installation)\n```\npython -m pip install --upgrade pip\npip install poetry\npoetry install\n```\n\n## Build Docs\n```\npoetry run sphinx-apidoc -f -o ./docs ../strike_api\ncd docs && poetry run make clean && poetry run make html\n```',
    'author': 'Thomas Cross',
    'author_email': 'tom.bz2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
