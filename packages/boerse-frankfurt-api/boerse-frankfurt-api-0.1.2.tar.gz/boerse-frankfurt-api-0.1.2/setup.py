# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boerse_frankfurt_api']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.28.1']

setup_kwargs = {
    'name': 'boerse-frankfurt-api',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Boerse Frankfurt API\n',
    'author': 'Martin Marmsoler',
    'author_email': 'martin.marmsoler@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
