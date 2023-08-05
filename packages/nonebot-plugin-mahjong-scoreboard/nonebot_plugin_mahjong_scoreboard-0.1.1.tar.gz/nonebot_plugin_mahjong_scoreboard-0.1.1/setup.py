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
['aiosqlite>=0.17.0,<0.18.0',
 'cachetools>=5.2.0,<6.0.0',
 'nonebot-adapter-onebot>=2.1.5,<3.0.0',
 'nonebot-plugin-sqlalchemy>=0.1.0,<0.2.0',
 'nonebot2>=2.0.0rc1,<3.0.0',
 'nonebot_plugin_apscheduler>=0.2.0,<0.3.0',
 'tzlocal>=4.2,<5.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-scoreboard',
    'version': '0.1.1',
    'description': '',
    'long_description': '日麻寄分器\n============\n\n支持适配器：[OneBot V11](https://onebot.adapters.nonebot.dev/)\n\n支持驱动器：[FastAPI](https://v2.nonebot.dev/docs/tutorial/choose-driver)\n\n## 配置\n\n### mahjong_scoreboard_database_conn_url\n\n数据库连接URL，必须使用异步SQLAlchemy驱动器。\n\n默认值：sqlite+aiosqlite:///mahjong_scoreboard.db\n\n### mahjong_scoreboard_callback_host\n\n回调HOST，若为非容器环境部署（go-cqhttp与nonebot均运行在同一环境）则保持默认值。若为Docker环境部署则设置为Docker容器名。用于上传文件时让go-cqhttp下载本机文件。\n\n默认值：127.0.0.1\n\n### mahjong_scoreboard_callback_port\n\n回调端口，保持默认值即可。\n\n默认值：与PORT保持一致即可\n\n## 指令\n\n### 对局\n\n- /新建对局 [四人南|四人东]\n- /结算对局 <成绩> [对局<编号>] [@<用户>] [<自风>]\n- /撤销结算对局 [对局<编号>] [@<用户>]\n- /设置对局PT <PT> [对局<编号>] [@<用户>]\n- /删除对局 [对局<编号>]\n- /设置对局进度 <进度> [对局<编号>]\n\n### 对局查询\n\n- /查询对局 [<编号>]\n- /个人最近对局 [@<用户>]\n- /群最近对局\n- /个人未完成对局 [@<用户>]\n- /群未完成对局\n- /导出赛季对局 [<代号>]\n- /导出所有对局\n\n### 赛季\n\n- /查询赛季 [<代号>]\n- /查询所有赛季\n- /新建赛季\n- /开启赛季 [<代号>]\n- /结束赛季\n- /删除赛季 [<代号>]\n\n### 赛季PT\n\n- /设置赛季PT <PT> [@<用户>]\n- /查询PT [@<用户>]\n- /查询榜单\n- /导出榜单\n\n以上命令格式中，以<>包裹的表示一个参数，以[]包裹的表示一个可选项。参数可通过任意顺序提供。\n\n## LICENSE\n\n> MIT License\n> \n> Copyright (c) 2022 ssttkkl\n> \n> Permission is hereby granted, free of charge, to any person obtaining a copy\n> of this software and associated documentation files (the "Software"), to deal\n> in the Software without restriction, including without limitation the rights\n> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n> copies of the Software, and to permit persons to whom the Software is\n> furnished to do so, subject to the following conditions:\n> \n> The above copyright notice and this permission notice shall be included in all\n> copies or substantial portions of the Software.\n> \n> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n> SOFTWARE.\n> \n',
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
