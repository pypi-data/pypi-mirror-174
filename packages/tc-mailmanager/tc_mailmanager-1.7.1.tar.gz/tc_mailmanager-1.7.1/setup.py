# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tc_mailmanager']

package_data = \
{'': ['*']}

install_requires = \
['sendgrid>=5,<6', 'tctc-envelopes==0.5']

setup_kwargs = {
    'name': 'tc-mailmanager',
    'version': '1.7.1',
    'description': "ToucanToco's cross-python-projects MailManager",
    'long_description': "[![Pypi-v](https://img.shields.io/pypi/v/tc_mailmanager.svg)](https://pypi.python.org/pypi/tc_mailmanager)\n[![Pypi-pyversions](https://img.shields.io/pypi/pyversions/tc_mailmanager.svg)](https://pypi.python.org/pypi/tc_mailmanager)\n[![Pypi-l](https://img.shields.io/pypi/l/tc_mailmanager.svg)](https://pypi.python.org/pypi/tc_mailmanager)\n[![Pypi-wheel](https://img.shields.io/pypi/wheel/tc_mailmanager.svg)](https://pypi.python.org/pypi/tc_mailmanager)\n[![GitHub Actions](https://github.com/ToucanToco/tc_mailmanager/workflows/CI/badge.svg)](https://github.com/ToucanToco/tc_mailmanager/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/ToucanToco/tc_mailmanager/branch/main/graph/badge.svg)](https://codecov.io/gh/ToucanToco/tc_mailmanager)\n\n# tc_mailmanager\n\nToucanToco's cross-python-projects MailManager\n\n## Installation\n\n```bash\n$ pip install tc_mailmanager\n```\n\n# Development\n\nYou need to install [poetry](https://python-poetry.org/) either globally or in a virtualenv.\nThen run `make install`\n",
    'author': 'Toucan Toco',
    'author_email': 'dev@toucantoco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ToucanToco/tc_mailmanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
