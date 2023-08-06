# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['orcha_watchdog']

package_data = \
{'': ['*']}

install_requires = \
['orcha==0.3.0-rc2', 'systemd-python>=234,<235']

setup_kwargs = {
    'name': 'orcha-watchdog',
    'version': '0.1.3',
    'description': 'Orcha pluggable for SystemD Watchdog integration',
    'long_description': None,
    'author': 'Javier Alonso',
    'author_email': 'jalonso@teldat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
