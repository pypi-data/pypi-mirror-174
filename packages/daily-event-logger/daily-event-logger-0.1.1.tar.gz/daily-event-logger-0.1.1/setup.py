# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daily_event_logger']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.0,<5.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'daily-event-logger',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jeffrey Serio',
    'author_email': 'hyperreal@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
