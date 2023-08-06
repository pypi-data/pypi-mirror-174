# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfcommon']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'djangorestframework>=3.10']

setup_kwargs = {
    'name': 'drfcommon',
    'version': '0.1.8.8',
    'description': 'a common tools for drf',
    'long_description': 'None',
    'author': 'tplinux',
    'author_email': '2363176358@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pydtools/drfcommon/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
