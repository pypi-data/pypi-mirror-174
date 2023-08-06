# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biliass', 'biliass.protobuf']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=4.21.9,<5.0.0']

entry_points = \
{'console_scripts': ['moelib = moelib.__main__:main']}

setup_kwargs = {
    'name': 'biliass',
    'version': '1.3.7.dev1',
    'description': '将 B 站 XML 弹幕转换为 ASS 弹幕',
    'long_description': '# biliass\n\n<p align="center">\n   <a href="https://python.org/" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/biliass?logo=python&style=flat-square"></a>\n   <a href="https://pypi.org/project/biliass/" target="_blank"><img src="https://img.shields.io/pypi/v/biliass?style=flat-square" alt="pypi"></a>\n   <a href="https://pypi.org/project/biliass/" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/biliass?style=flat-square"></a>\n   <a href="https://actions-badge.atrox.dev/yutto-dev/biliass/goto?ref=main"><img alt="Build Status" src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fyutto-dev%2Fbiliass%2Fbadge%3Fref%3Dmain&style=flat-square&label=Test" /></a>\n   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/yutto-dev/biliass?style=flat-square"></a>\n   <a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square" alt="Gitmoji"></a>\n</p>\n\nbiliass，只是 Danmaku2ASS 的 bilili 与 yutto 适配版\n\n原版：<https://github.com/m13253/danmaku2ass>\n\n仅支持 bilibili 弹幕，支持 XML 弹幕和 Protobuf 弹幕\n\n## Install\n\n```bash\npip install biliass\n```\n\n## Usage\n\n```bash\n# XML 弹幕\nbiliass danmaku.xml -s 1920x1080 -o danmaku.ass\n# protobuf 弹幕\nbiliass danmaku.pb -s 1920x1080 -f protobuf -o danmaku.ass\n```\n\n```python\nfrom biliass import Danmaku2ASS\n\n# xml\nDanmaku2ASS(\n    xml_text_or_bytes,\n    width,\n    height,\n    input_format="xml",\n    reserve_blank=0,\n    font_face="sans-serif",\n    font_size=width / 40,\n    text_opacity=0.8,\n    duration_marquee=15.0,\n    duration_still=10.0,\n    comment_filter=None,\n    is_reduce_comments=False,\n    progress_callback=None,\n)\n\n# protobuf\nDanmaku2ASS(\n    protobuf_bytes, # only bytes\n    width,\n    height,\n    input_format="protobuf",\n    reserve_blank=0,\n    font_face="sans-serif",\n    font_size=width / 40,\n    text_opacity=0.8,\n    duration_marquee=15.0,\n    duration_still=10.0,\n    comment_filter=None,\n    is_reduce_comments=False,\n    progress_callback=None,\n)\n```\n\n## TODO\n\n- 导出 bilibili 网页上的弹幕设置，并导入到 biliass\n',
    'author': 'm13253',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yutto-dev/biliass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
