# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_who_is_suspect']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.4.1,<0.5.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-who-is-suspect',
    'version': '0.1.0',
    'description': '谁是卧底',
    'long_description': '# 谁是卧底 0.1.0\n\n基于[ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)开发的 谁是卧底 小游戏\n\n任何问题欢迎issue\n\n## 安装插件\n\n`poetry add nonebot-plugin-ayaka-who-is-suspect`\n\n## 导入插件\n\n修改nonebot2  `bot.py` \n\n```python\nnonebot.load_plugin("ayaka_who_is_suspect")\n```\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/games/who-is-suspect\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
