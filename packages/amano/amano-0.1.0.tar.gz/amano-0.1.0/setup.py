# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amano']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.57,<2.0.0',
 'boto>=2.49.0,<3.0.0',
 'botocore>=1.27.57,<2.0.0',
 'chili>=1.7.0,<2.0.0',
 'gid>=1.0.1,<2.0.0',
 'mypy-boto3-dynamodb>=1.24.36,<2.0.0']

setup_kwargs = {
    'name': 'amano',
    'version': '0.1.0',
    'description': 'Abstraction Layer for Amazon DynamoDB',
    'long_description': None,
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@kaizenreporting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
