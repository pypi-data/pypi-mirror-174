# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['ayaka_who_is_suspect']
install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.3.9,<0.4.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-who-is-suspect',
    'version': '0.0.11',
    'description': '谁是卧底',
    'long_description': '# 谁是卧底 0.0.11\n\n基于[ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)开发的 谁是卧底 小游戏\n\n任何问题欢迎issue\n\n[仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect) - \n[文档](https://bridgel.github.io/ayaka_doc/games/who-is-suspect)\n\n# How to start\n\n## 安装插件\n\n`poetry add nonebot-plugin-ayaka-who-is-suspect`\n\n## 导入插件\n\n修改nonebot2  `bot.py` \n\n```python\nnonebot.load_plugin("ayaka_who_is_suspect")\n```\n\n## 导入数据\n\n将本仓库的data文件夹（这是题库，可以自行修改，第一个是普通人，第二个是卧底词），放到nonebot的工作目录下\n\n之后运行nonebot即可\n\n# 指令\n\nhttps://bridgel.github.io/ayaka_doc/games/who-is-suspect\n\n## 没有打开游戏应用时\n\n指令|效果\n-|-\nhelp 谁是卧底 | 查看帮助\n谁是卧底 | 打开游戏应用，将创建一个游戏房间\n\n## 房间内\n\n指令|效果 \n-|-\njoin/加入 | 加入房间\nleave/离开 | 离开房间\nstart/begin/开始 | 开始游戏\ninfo/信息 | 展示已加入房间的人员列表\nexit/退出 | 关闭游戏 \n\n注意，由于要私聊关键词，所以参与人都要提前加bot好友哦\n\n## 游戏进行时\n\n指令|效果 \n-|-\nvote \\<at> | 请at你要投票的对象，一旦投票无法更改\ninfo/信息 | 展示投票情况\nforce_exit | 强制关闭游戏，有急事可用\n\n注意：vote和at间加个空格（一般情况下不加也行，但如果你是复制了其他人的投票，那么要加一个空格）\n\n注意：游戏进行时没有任何发言顺序控制，玩家可以自行协商一个发言顺序，或者自由发言，可以约定发言一轮，也可以约定发多轮后再投票，都可以，不做限制\n\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
