# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['burner']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4==4.11.1', 'click==8.1.3', 'requests==2.28.1']

entry_points = \
{'console_scripts': ['burner = burner.__main__:cli']}

setup_kwargs = {
    'name': 'burner',
    'version': '0.1.0',
    'description': "Script to interact with SimSMS's website.",
    'long_description': 'None',
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
