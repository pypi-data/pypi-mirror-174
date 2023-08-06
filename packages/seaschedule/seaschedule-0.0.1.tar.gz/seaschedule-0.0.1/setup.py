# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'config': 'src\\config', 'utils': 'src\\utils'}

packages = \
['config', 'seaschedule', 'utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0',
 'paramiko>=2.11.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['ss = seaschedule.__main__:main']}

setup_kwargs = {
    'name': 'seaschedule',
    'version': '0.0.1',
    'description': 'Get sea schedules from Maersk and other shipping lines.',
    'long_description': '# seaschedule\nGet sea schedules from Maersk and other shipping lines.\n\n## Installation\nFrom [PyPI](https://pypi.org/project/seaschedule/):\n\n    python -m pip install seaschedule\n\n## Setup\nThe following setup must be done before running seaschedule:\n1. Create below environment variables in your OS environment:\n    * `SS_SMTP_HOST`: SMTP host for sending notification emails\n    * `SS_IB_SFTP_USER`: SFTP user for uploading schedule files to Information Broker\n    * `SS_IB_SFTP_PWD`: SFTP password for uploading schedule files to Information Broker\n    * `SS_MAEU_API_KEY`: API key given by Maersk \n<br/><br/>\n2. Specify below directory paths in `site-packages\\seaschedule\\config\\config.toml` for storing the schedule data files and log files. For example:\n    ```\n    [environment]\n    directory.data = "/home/user1/seaschedule/data"\n    directory.log = "/home/user1/seaschedule/log"\n\n    # Windows\n    directory.data = "C:\\Users\\user1\\Documents\\seaschedule\\data"\n    directory.log = "C:\\Users\\user1\\Documents\\seaschedule\\data"\n    ```\n\n## How to Use\nseaschedule is a console application, named `seaschedule`.\n\n    >>> python -m seaschedule\n',
    'author': 'Alex Cheng',
    'author_email': 'alex28.biz@gmail.com',
    'maintainer': 'Alex Cheng',
    'maintainer_email': 'alex28.biz@gmail.com',
    'url': 'https://github.com/alexcheng628/seaschedule',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
