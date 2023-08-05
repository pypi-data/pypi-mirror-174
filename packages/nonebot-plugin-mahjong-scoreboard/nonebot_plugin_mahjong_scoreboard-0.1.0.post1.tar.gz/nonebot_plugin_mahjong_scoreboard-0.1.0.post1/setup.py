# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_mahjong_scoreboard',
 'nonebot_plugin_mahjong_scoreboard.controller',
 'nonebot_plugin_mahjong_scoreboard.controller.interceptor',
 'nonebot_plugin_mahjong_scoreboard.controller.mapper',
 'nonebot_plugin_mahjong_scoreboard.model',
 'nonebot_plugin_mahjong_scoreboard.model.orm',
 'nonebot_plugin_mahjong_scoreboard.service',
 'nonebot_plugin_mahjong_scoreboard.utils']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.26.0,<0.27.0',
 'cachetools>=5.2.0,<6.0.0',
 'nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot-plugin-sqlalchemy>=0.1.0,<0.2.0',
 'nonebot2>=2.0.0rc1,<3.0.0',
 'nonebot_plugin_apscheduler>=0.2.0,<0.3.0',
 'tzlocal>=4.2,<5.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-scoreboard',
    'version': '0.1.0.post1',
    'description': '',
    'long_description': '日麻寄分器\n============\n\n## 配置\n\n### mahjong_scoreboard_database_conn_url\n\n数据库连接URL，必须为postgresql+asyncpg\n\n举例：postgresql+asyncpg://username:password@host:5432/database\n\n## 指令\n\n### 对局\n\n- 新建对局\n- 结算对局\n- 撤销结算对局\n- 设置对局PT\n- 删除对局\n- 设置对局进度\n\n### 对局查询\n\n- 查询对局\n- 个人最近对局\n- 群最近对局\n- 个人未完成对局\n- 群未完成对局\n- 导出赛季对局\n- 导出所有对局\n- \n### 赛季\n\n- 查询赛季\n- 查询所有赛季\n- 新建赛季\n- 开启赛季\n- 结束赛季\n- 删除赛季\n\n### 赛季PT\n\n- 设置赛季PT\n- 查询PT\n- 查询榜单\n- 导出榜单\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-mahjong-scoreboard',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
