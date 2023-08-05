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
    'version': '0.3.11',
    'description': 'a useful plugin providing convinient tools for the development of textual game on QQ',
    'long_description': '<div align="center">\n\n# Ayaka 0.3.11\n\n适用于[nonebot2机器人](https://github.com/nonebot/nonebot2)的文字游戏开发辅助插件 \n\n<img src="https://img.shields.io/badge/python-3.8%2B-blue">\n\n[仓库](https://github.com/bridgeL/nonebot-plugin-ayaka) - \n[文档](https://bridgel.github.io/ayaka_doc/)\n\n</div>\n\nayaka 通过二次封装nonebot2提供的api，提供专用api，便于其他文字游戏插件（ayaka衍生插件）的编写\n\n单独安装ayaka插件没有意义，ayaka插件的意义在于帮助ayaka衍生插件实现功能\n\n任何问题欢迎issue\n\n## 已有的ayaka衍生插件\n\n- [示例库](https://github.com/bridgeL/ayaka_plugins)\n- [小游戏合集](https://github.com/bridgeL/nonebot-plugin-ayaka-games)\n\n## 安装\n\n1. 修改nonebot工作目录下的`pyproject.toml`文件，将`python = "^3.7.3"`修改为`python = "^3.8.0"`\n2. `poetry add nonebot-plugin-ayaka` \n3. `poetry run playwright install chromium`\n\n注意：\n\n如果没有用到无头浏览器截图的功能，可忽略最后一步\n\n不需要特意在`bot.py`中加载ayaka插件，只要正常加载ayaka衍生插件即可\n\nayaka衍生插件中也只需正常导入ayaka就行 `from ayaka import AyakaApp`\n\n## 配置\n\n推荐配置（非强制要求）\n```\nCOMMAND_START=["#"]\nCOMMAND_SEP=[" "]\n```\n\n## 文档\nhttps://bridgel.github.io/ayaka_doc/\n',
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
