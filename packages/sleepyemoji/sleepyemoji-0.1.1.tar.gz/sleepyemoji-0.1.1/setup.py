# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sleepyemoji', 'sleepyemoji.toolchain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sleepyemoji',
    'version': '0.1.1',
    'description': 'Print all the emojis that sleepyboy thinks are worthwhile!',
    'long_description': '# **Emoji**\n*A command line emoji tool, for the >%20 of emojis you actually care about.*\n\n<br />\n\n## **Mechanical Overview**\nAfter setting up **Envi**, run `emoji [-h|--help]` to display this message:\n```txt\nThis tool prints emojis of one or more catgories, each defined in their own file.\nEmojis are given along with their unicode value, discord shorthand, and ios descriptor.\n\nFor the official emoji index:\n  https://unicode.org/emoji/charts/full-emoji-list.html\n\n\nProvide 1 or more options of various emoji categories, or simply request all of them.\n--------------\nAll:\n  ./main.py [-C|--complete]\nCategories:\n  /main.py [*flags]\n    [-A|--animals]\n    [-F|--faces]\n    [-H|--hands]\n    [-I|--icons]\n    [-P|--people]\n    [--combos|--combinations]\nExample:\n  ./main.py -A -H\nInfo:\n  ./main.py [-h|--help]\n--------------\n```\n\n<br /><hr>\n\n## **Contributing**\nThis tool is kept in **Envi**, where emoji data is added in `emojis/toolchain` in the corresponding folders.\n\nRemember to pull before you push!\n\n<br /><hr />\n\n## **References**\n- [Emoji Index](https://unicode.org/emoji/charts/full-emoji-list.html)',
    'author': 'anthonybench',
    'author_email': 'anythonybenchyep@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
