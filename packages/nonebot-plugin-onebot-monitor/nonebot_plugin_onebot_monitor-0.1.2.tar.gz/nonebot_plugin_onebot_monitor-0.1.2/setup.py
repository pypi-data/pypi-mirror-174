# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_onebot_monitor', 'nonebot_plugin_onebot_monitor.models']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.17.0,<0.18.0',
 'cachetools>=5.2.0,<6.0.0',
 'nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-sqlalchemy>=0.1.0,<0.2.0',
 'nonebot2>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-onebot-monitor',
    'version': '0.1.2',
    'description': '',
    'long_description': 'None',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
