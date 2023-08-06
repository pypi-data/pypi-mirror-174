# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daily_event_logger']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.0,<5.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['elog = daily_event_logger.elog:main']}

setup_kwargs = {
    'name': 'daily-event-logger',
    'version': '0.1.3',
    'description': 'A utility for logging daily tasks and events.',
    'long_description': '# daily-event-logger\n\nThis is a little utility I use for logging my daily activities and events. It is written in Python.\n\n## Install\n\n```bash\npython3 -m pip install daily-event-logger\n```\n\n## Usage\n\nTo change the directory where elogs are stored, set a shell environment variable ELOG_DIR. To make this change permament, set the following in your shell configuration:\n\n```bash\nexport ELOG_DIR="/path/to/elog/dir"\n```\n\nOtherwise, the default elog directory will be `~/elogs`.\n\nTo get started, add your first elog entry! This will create a JSON file under your elog directory for the day and ensure the elog directory exists. E.g.:\n\n```bash\nelog add -m "Started new elog. Yay!"\n```\n\n```bash\nusage: elog [-h] [-v] {add,edit,rm,ls,lsfiles,search} ...\n\npositional arguments:\n  {add,edit,rm,ls,lsfiles,search}\n\noptions:\n  -h, --help            show this help message and exit\n  -v, --version         Print version information\n```\n\n### Example list output\n![screenshot.png](/screenshot.png)\n\n',
    'author': 'Jeffrey Serio',
    'author_email': 'hyperreal@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hyperreal64/daily-event-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
