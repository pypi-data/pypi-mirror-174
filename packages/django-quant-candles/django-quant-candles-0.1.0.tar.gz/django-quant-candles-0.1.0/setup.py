# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quant_candles']

package_data = \
{'': ['*']}

install_requires = \
['django-filter',
 'django-storages',
 'djangorestframework',
 'httpx',
 'pandas',
 'pyarrow',
 'randomname']

setup_kwargs = {
    'name': 'django-quant-candles',
    'version': '0.1.0',
    'description': 'Django Quant Candles downloads and aggregate candlesticks from tick data',
    'long_description': '',
    'author': 'Alex',
    'author_email': 'globophobe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/globophobe/django-quant-candles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
