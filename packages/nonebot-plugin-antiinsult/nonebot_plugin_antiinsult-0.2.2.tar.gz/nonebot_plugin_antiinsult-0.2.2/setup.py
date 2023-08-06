# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_antiinsult']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.5,<3.0.0', 'nonebot2>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-antiinsult',
    'version': '0.2.2',
    'description': 'Anti-insult in NoneBot2',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-antiinsult\n  \n_✨ NoneBot 反嘴臭插件 ✨_\n  \n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-antiinsult">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-antiinsult.svg" alt="pypi">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</a>\n\n</div>\n\n  \n## 📖 介绍\n  \n**本插件为被动插件**  \n  \n检测到有用户 `@机器人` 并嘴臭时将其临时屏蔽(bot重启后失效)  \n当bot为群管理时会请对方喝昏睡红茶(禁言)  \n  \n超级用户不受临时屏蔽影响 _~~但是会被昏睡红茶影响~~_ (当bot的群权限比超级用户高的时候会请超级用户喝昏睡红茶)  \n  \n**增删屏蔽词库:**  \n聊天发送 **添加/删除屏蔽词 词1 词2 词3 ...**  \n  \nP.S. 你说从聊天界面查看屏蔽词库? 噢, 我亲爱的老伙计, 你怕是疯了!  \n  \n  \n## 💿 安装\n  \n**使用 nb-cli 安装**  \n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装  \n```bash\nnb plugin install nonebot-plugin-antiinsult\n```\n  \n**使用 pip 安装**  \n```bash\npip install nonebot-plugin-antiinsult\n```\n  \n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n```python\nnonebot.load_plugin(\'nonebot_plugin_antiinsult\')\n```\n  \n\n## 🎉 使用\n### 指令表\n\n<table> \n  <tr align="center">\n    <th> 指令 </th>\n    <th> 权限 </th>\n    <th> 需要@ </th>\n    <th> 范围 </th>\n    <th> 说明 </th>\n  </tr>\n  <tr align="center">\n    <td> 添加屏蔽词 xxx </td>\n    <td> 主人 </td>\n    <td> 否 </td>\n    <td> 私聊 | 群聊 </td>\n    <td rowspan="2"> 可输入多个,<br>用空格隔开 </td>\n  </tr>\n  <tr align="center">\n    <td> 删除屏蔽词 xxx </td>\n    <td> 主人 </td>\n    <td> 否 </td>\n    <td> 私聊 | 群聊 </td>\n  </tr>\n</table>\n',
    'author': '月ヶ瀬',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tkgs0/nonebot-plugin-antiinsult',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
