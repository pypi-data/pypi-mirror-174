# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firestone_lib', 'firestone_lib.resources', 'firestone_lib.resources.logging']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'click>=8.1.3,<9.0.0', 'setuptools>=65.5.0,<66.0.0']

setup_kwargs = {
    'name': 'firestone-lib',
    'version': '0.1.0',
    'description': 'Library to help build OpneAPI, AsyncAPI and gRPC specs based off one or more resource json schema files',
    'long_description': '![PR Build](https://github.com/ebourgeois/firestone-lib/actions/workflows/pr.yml/badge.svg)\n\n\n# firestone-lib\n\nThus library is primarily used by the firestone and anyone using the firestone project.\n\n# building and testing\n\n```\nbrew install poetry\npoetry install\npoetry build\npoetry run pytest test\n```\n',
    'author': 'Erick Bourgeois',
    'author_email': 'erick@jeb.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
