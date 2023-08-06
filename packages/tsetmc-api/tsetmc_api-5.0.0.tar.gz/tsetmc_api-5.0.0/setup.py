# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

packages = \
['tsetmc_api',
 'tsetmc_api.day_details',
 'tsetmc_api.group',
 'tsetmc_api.market_map',
 'tsetmc_api.market_watch',
 'tsetmc_api.symbol']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'jdatetime>=4.1.0,<5.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'schedule>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'tsetmc-api',
    'version': '5.0.0',
    'description': 'simple package to communicate and crawl data from tsetmc.com (Tehran Stock Exchange Website)',
    'long_description': 'None',
    'author': 'Mahdi Sadeghi',
    'author_email': 'mahdi74sadeghi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mahs4d/tsetmc-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
