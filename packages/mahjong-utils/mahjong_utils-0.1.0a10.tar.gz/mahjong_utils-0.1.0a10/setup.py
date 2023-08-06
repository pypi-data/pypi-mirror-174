# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mahjong_utils',
 'mahjong_utils.internal',
 'mahjong_utils.internal.utils',
 'mahjong_utils.models',
 'mahjong_utils.yaku']

package_data = \
{'': ['*']}

install_requires = \
['lazy>=1.5,<2.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'mahjong-utils',
    'version': '0.1.0a10',
    'description': '',
    'long_description': 'mahjong-utils\n========\n\n已实现功能：\n\n- [x] 获取番符对应和牌点数\n- [x] 向听数、进张分析\n- [x] 和了分析（役种、番数、符数）\n\n## 获取番符对应和牌点数\n\n```python\nfrom mahjong_utils.point_by_han_hu import get_parent_point_by_han_hu, get_child_point_by_han_hu\n\n# 获取亲家X番Y符的点数，返回(荣和点数, 自摸各家点数)\nparent_ron, parent_tsumo = get_parent_point_by_han_hu(3, 40)\n# parent_ron == 7700\n# parent_tsumo == 2600\n\n# 获取子家X番Y符的点数，返回(荣和点数, 自摸庄家点数, 自摸闲家点数)\nchild_ron, child_tsumo_parent, child_tsumo_child = get_child_point_by_han_hu(3, 40)\n# child_ron == 5200\n# child_tsumo_child == 1300\n# child_tsumo_parent == 2600\n```\n\n## 向听数、进张分析\n\n```python\nfrom mahjong_utils.models.tile import parse_tiles\nfrom mahjong_utils.shanten import shanten\n\n# 向听数、进张分析（未摸牌状态）\nresult = shanten(parse_tiles("34568m235p68s"))\n# result.shanten == 2\n# result.advance == {3M, 6M, 7M, 8M, 1P, 2P, 3P, 4P, 5P, 6S, 7S, 8S}\n\n# 向听数、进张分析（已摸牌状态）\nresult = shanten(parse_tiles("34568m235p368s"))\n# result.shanten == 2\n# result.discard_to_advance == {\n#   5P: {3M, 6M, 7M, 8M, 1P, 2P, 3P, 4P, 3S, 6S, 7S, 8S},\n#   3S: {3M, 6M, 7M, 8M, 1P, 2P, 3P, 4P, 5P, 6S, 7S, 8S},\n#   2P: {3M, 6M, 7M, 8M, 3P, 4P, 5P, 3S, 6S, 7S, 8S},\n#   8M: {3M, 6M, 1P, 2P, 4P, 5P, 3S, 7S},\n#   3M: {8M, 1P, 2P, 4P, 5P, 3S, 7S},\n#   6M: {8M ,1P, 2P, 4P, 5P, 3S, 7S},\n#   6S: {7M, 1P, 2P, 4P, 5P, 3S, 8S},\n#   8S: {7M, 1P, 2P, 4P, 5P, 3S, 6S},\n#   3P: {7M, 2P, 5P, 3S, 7S},\n# }\n```\n\n## 和了分析\n\n```python\nfrom mahjong_utils.hora import build_hora\nfrom mahjong_utils.models.tile import parse_tiles, tile\nfrom mahjong_utils.models.wind import Wind\nfrom mahjong_utils.models.furo import parse_furo\nfrom mahjong_utils.yaku.common import self_wind, round_wind\n\n# 和了分析\nhora = build_hora(\n    tiles=parse_tiles("12233466m11z"),\n    furo=[parse_furo("789p")],\n    agari=tile("1z"),\n    tsumo=True,\n    dora=4,\n    self_wind=Wind.east,\n    round_wind=Wind.east\n)\n\n# hora.yaku == {self_wind, round_wind}\n# hora.han == 6\n# hora.hand.hu == 30\n# hora.parent_point == (18000, 6000)\n# hora.child_point == (12000, 6000, 3000)\n```',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
