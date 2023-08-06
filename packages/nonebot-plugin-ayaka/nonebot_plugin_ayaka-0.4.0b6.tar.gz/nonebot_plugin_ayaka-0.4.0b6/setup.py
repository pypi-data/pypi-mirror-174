# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot2>=2.0.0b5,<3.0.0',
 'playwright>=1.27.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka',
    'version': '0.4.0b6',
    'description': 'a useful plugin providing convinient tools for the development of textual game on QQ',
    'long_description': '<div align="center">\n\n# Ayaka 0.4.0b6\n\n适用于[nonebot2机器人](https://github.com/nonebot/nonebot2)的文字游戏开发辅助插件 \n\n<img src="https://img.shields.io/badge/python-3.8%2B-blue">\n\n[仓库](https://github.com/bridgeL/nonebot-plugin-ayaka)\n\n**0.4.x 目前没有文档支持**\n\n</div>\n\nayaka 通过二次封装nonebot2提供的api，提供专用api，便于其他文字游戏插件（ayaka衍生插件）的编写\n\n单独安装ayaka插件没有意义，ayaka插件的意义在于帮助ayaka衍生插件实现功能\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bridgel.github.io/ayaka_doc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
