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
    'version': '5.0.2',
    'description': 'simple package to communicate and crawl data from tsetmc.com (Tehran Stock Exchange Website)',
    'long_description': '# TSETMC-API\n\nThis library is for getting data from [tsetmc](http://tsetmc.com) website. It is divided into 5 subcomponents:\n\n## Installation\n\nYou can install this library using the following command:\n\n`pip install tsetmc-api`\n\n## Usage\n\n- **symbol:** working with main symbol page and live data (e.g. [this page](http://www.tsetmc.com/loader.aspx?ParTree=151311&i=43362635835198978))\n- **market_watch:** getting data visible from [market watch page](http://www.tsetmc.com/Loader.aspx?ParTree=15131F)\n- **day_details:** working with details of a symbol in a single day of history (e.g. [this page](http://cdn.tsetmc.com/History/43362635835198978/20221029))\n- **market_map:** getting data visible in [market map page](http://main.tsetmc.com/marketmap)\n- **group:** getting list of available symbol groups\n\n### Symbol Component (tsetmc_api.symbol)\n\n![Symbol Component](https://github.com/mahs4d/tsetmc-api/blob/master/docs/images/Symbol.png?raw=true)\n\n### Market Watch Component (tsetmc_api.market_watch)\n\n![Market Watch Component](https://github.com/mahs4d/tsetmc-api/blob/master/docs/images/MarketWatch.png?raw=true)\n\n### Day Details Component (tsetmc_api.day_details)\n\n![Day Details Component](https://github.com/mahs4d/tsetmc-api/blob/master/docs/images/DayDetails.png?raw=true)\n\n### Market Map Component (tsetmc_api.market_map)\n\n![Market Map Component](https://github.com/mahs4d/tsetmc-api/blob/master/docs/images/MarketMap.png?raw=true)\n\n### Group Component (tsetmc_api.group)\n\nGroup component currently only has one function (`get_all_groups`) which returns all the symbol groups.\n\n### Errors\n\nTsetmc sometimes returns 403 and you should retry.\n\n## Support and Donation\nIf this repository helped you, please support it by giving a star (:star:).\nFor donation please contact me at [mahdi74sadeghi@gmail.com](mailto:mahdi74sadeghi@gmail.com).\n',
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
