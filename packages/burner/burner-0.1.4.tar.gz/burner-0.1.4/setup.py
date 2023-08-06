# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['burner', 'burner.resources']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1', 'click==8.1.3', 'requests==2.28.1']

entry_points = \
{'console_scripts': ['burner = burner.__main__:cli']}

setup_kwargs = {
    'name': 'burner',
    'version': '0.1.4',
    'description': "Script to interact with SimSMS's website.",
    'long_description': '# Burner\n\nEasy to use script to determine the cheapest price for [SimSMS](https://simsms.org/).\n\n## Installation\n\n### With Pip\n\n```bash\npip install burner\n```\n\n### With Poetry\n\n```bash\npoetry add git+https://github.com/ramadan8/Burner.git\n```\n\n### Manual\n\n```bash\ngit clone https://github.com/ramadan8/Burner --depth 1\npoetry install\n```\n\n## Usage\n\nUse the following command to find the code for the service you want.\n\n```bash\nburner services\n```\n\nThen use the following command to find the price list for the service.\n\n```bash\nburner prices opt29 # This will get the price list for Telegram.\n```\n\nIf you want to refresh the cache for the prices to a newer version, run the following\ncommand.\n\n```bash\nburner --authorization <apikey> reset\n```\n',
    'author': 'Aidan',
    'author_email': 'ramadan8@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ramadan8/Burner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
