# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nonebot_plugin_mahjong_utils',
 'nonebot_plugin_mahjong_utils.interceptors',
 'nonebot_plugin_mahjong_utils.matchers',
 'nonebot_plugin_mahjong_utils.utils']

package_data = \
{'': ['*']}

install_requires = \
['mahjong-utils>=0.1.0a4,<0.2.0', 'nonebot2>=2.0.0rc1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mahjong-utils',
    'version': '0.1.6.post1',
    'description': '',
    'long_description': 'nonebot-plugin-mahjong-utils\n========\n\n手牌分析：\n- 输入手牌代码，输出向听数（未摸牌状态）、牌理（已摸牌、未和牌状态）或和牌分析（已摸牌、已和牌状态）。\n- 手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。\n- 例：23445633p777s 0990m 立直 一发 dora3\n\n番符点数查询：\n- 输入x番y符，输出亲家/子家的自摸/荣和得点\n\n## Special Thanks\n\n-  [nonebot/nonebot2](https://github.com/nonebot/nonebot2)\n-  [ssttkkl/mahjong-utils](https://github.com/ssttkkl/mahjong-utils) ~~我谢我自己~~\n\n## LICENSE\n\nMIT\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ssttkkl/nonebot-plugin-mahjong-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
