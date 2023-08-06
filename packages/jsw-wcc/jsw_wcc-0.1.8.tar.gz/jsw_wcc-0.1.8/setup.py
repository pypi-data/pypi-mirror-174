# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_wcc']

package_data = \
{'': ['*'], 'jsw_wcc': ['font/*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0']

entry_points = \
{'console_scripts': ['wcc = jsw_wcc.main:cli']}

setup_kwargs = {
    'name': 'jsw-wcc',
    'version': '0.1.8',
    'description': 'Add water mark for image based on python.',
    'long_description': "# jsw-wcc(marker.py)\n> 为图片添加文字水印\n> 可设置文字**大小、颜色、旋转、间隔、透明度**\n\n## installation\n```shell\npip install jsw-wcc -U\n```\n\n# usage\n> 需要 PIL 库 `pip install Pillow`\n\n```\nusage: wcc [-h] [-f FILE] [-m MARK] [-o OUT] [-c COLOR] [-s SPACE] [-a ANGLE] [--font-family FONT_FAMILY] [--font-height-crop FONT_HEIGHT_CROP] [--size SIZE]\n                 [--opacity OPACITY] [--quality QUALITY]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f FILE, --file FILE  image file path or directory\n  -m MARK, --mark MARK  watermark content\n  -o OUT, --out OUT     image output directory, default is ./output\n  -c COLOR, --color COLOR\n                        text color like '#000000', default is #8B8B1B\n  -s SPACE, --space SPACE\n                        space between watermarks, default is 75\n  -a ANGLE, --angle ANGLE\n                        rotate angle of watermarks, default is 30\n  --font-family FONT_FAMILY\n                        font family of text, default is './font/青鸟华光简琥珀.ttf'\n                        using font in system just by font file name\n                        for example 'PingFang.ttc', which is default installed on macOS\n  --font-height-crop FONT_HEIGHT_CROP\n                        change watermark font height crop\n                        float will be parsed to factor; int will be parsed to value\n                        default is '1.2', meaning 1.2 times font size\n                        this useful with CJK font, because line height may be higher than size\n  --size SIZE           font size of text, default is 50\n  --opacity OPACITY     opacity of watermarks, default is 0.15\n  --quality QUALITY     quality of output images, default is 90\n```\n\n# 效果\n`python marker.py -f ./input/test.png -m 添加水印`\n\n![](/output/test.png?raw=true)\n",
    'author': 'afeiship',
    'author_email': '1290657123@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
