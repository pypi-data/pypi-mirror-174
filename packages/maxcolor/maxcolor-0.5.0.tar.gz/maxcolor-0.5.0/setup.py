# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxcolor']
install_requires = \
['maxconsole>=0.2.0,<0.3.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['gradient = maxcolor:gradient',
                     'gradient_panel = maxcolor:gradient_panel',
                     'maxcolor = maxcolor:main',
                     'rainbow = maxcolor:rainbow']}

setup_kwargs = {
    'name': 'maxcolor',
    'version': '0.5.0',
    'description': 'A module to genereate gradient text and rich panels.',
    'long_description': '---\nTitle: README.md\nPath: README.md\nAuthor: Max Ludden\nDate: 2022-10-31 7:28 AM EST\nCSS: static/style.css\n...\n\n# maxcolor 0.5.0\n\n## Purpose\n\nThis is a collection of helper scripts to work with rich renderables.\n\n<br />\n\n## Features from Textualize/Rich:\n\n<br />\n\n- Provides a helper function to allow for rich to easily print gradient text.\n- Provides a helper function to allow for rich to easily print a gradient text to a panel.\n\n<br />\n\n## Installation\n\n<br />\n\n#### Install from Pip\n\n```Python\npip install maxcolor\n```\n\n<br />\n\n#### Install from Pipx\n\n```Python\npipx install maxcolor\n```\n\n<br />\n\n#### Install from Pipx\n\n```Python\npython add maxcolor\n```\n\n<br />\n<hr />\n<br />\n\n## Usage\n\n<br />\n\nThe following are available to import from `maxcolor`:\n\n### Color Regular Expressions\n\n```Python\nfrom maxcolor import HEX_REGEX, ANSI_REGEX, RGB_REGEX, COLOR_REGEX\n\nhex_result = re.match(HEX_REGEX, "#FF0000")\nansi_result = re.match(ANSI_REGEX, "124")\nrgb_result = re.match(RGB_REGEX, "255, 0, 0")\ncolor_result = re.match(COLOR_REGEX, "#FF0000 123 255, 0, 0")\n```\n\n### Color Conversion Functions\n```python\nfrom maxcolor import hex_to_rgb, rgb_to_hex\n\nrgb_color = hex_to_rgb("#FF0000") # (255, 0, 0)  # RGB tuple\n\nhex_color = rgb_to_hex(255, 0, 0) # "#FF0000"  # Hex string\n```\n\n### Gradient Color Functions\n```Python\nfrom maxcolor import gradient, rainbow, gradient_panel\n\nconsole = get_console(get_theme())\n\nconsole.print(\n    gradient("Hello World!")\n)\n```\n\n![gradient.png](static/gradient.png)\n\nThe gradient function will allow you to print multicolor gradients colored text. THe gradient function takes a string, an optional number of colors (defaults to 4), and an optional justification (defaults to "left").\n\nThe rainbow function is simply a the gradient function with the maximum number of colors, 10. And since it spans the entire color spectrum, it\'s a great way to print a rain.\n```Python\nconsole.print(\n    gradient(\n        "Sunt sit est labore elit ut laboris est. Aute cupidatat sit officia deserunt sint adipisicing et minim aliqua enim. Tempor eiusmod dolore excepteur dolore id aliquip enim incididunt ex. Non ipsum eu cillum proident ex. Officia deserunt consequat adipisicing est eiusmod nisi tempor aliquip proident ut in sunt nisi ullamco."\n    )\n)\nconsole.print(\n    rainbow(\n        "Sunt sit est labore elit ut laboris est. Aute cupidatat sit officia deserunt sint adipisicing et minim aliqua enim. Tempor eiusmod dolore excepteur dolore id aliquip enim incididunt ex. Non ipsum eu cillum proident ex. Officia deserunt consequat adipisicing est eiusmod nisi tempor aliquip proident ut in sunt nisi ullamco.\\n\\n"\n    )\n)\n```\n\n#### Gradient (top text)\n\n<br />\n\n![gradient_rainbow](static/gradient_rainbow.png)\n\n#### Rainbow (bottom text)\n\n<hr />\n<br />\n\n## Gradient Panel\nSomtimes you need something more formal than a gradient, though. For that, you can use the gradient_panel function. This function takes a string, an optional number of colors (defaults to 4), and an optional justification (defaults to "left"). It will return a panel with the gradient text, and optionally, gradient title.\n\n```python\ntext = "\\tEnim tempor veniam proident. Reprehenderit deserunt do duis laboris laborum consectetur fugiat deserunt officia officia eu consequat. Aute sint occaecat adipisicing eu aute. Eu est laborum enim deserunt fugiat nostrud officia do ad cupidatat enim amet cillum amet. Consectetur occaecat ex quis irure cupidatat amet occaecat ad sit adipisicing pariatur est velit mollit voluptate. Eiusmod deserunt nisi voluptate irure. Sunt irure consectetur veniam dolore elit officia et in labore esse esse cupidatat labore. Fugiat enim irure ipsum eiusmod consequat irure commodo cillum.\\n\\n\\tReprehenderit ea quis aliqua qui labore enim consequat ea nostrud voluptate amet reprehenderit consequat sunt. Ad est occaecat mollit qui sit enim do esse aute sint nulla sint laborum. Voluptate veniam ut Lorem eiusmod id veniam amet ipsum labore incididunt. Ex in consequat voluptate mollit nisi incididunt pariatur ipsum ut eiusmod ut cupidatat elit. Eu irure est ad nulla exercitation. Esse elit tempor reprehenderit ipsum eu officia sint.\\n\\n\\tCupidatat officia incididunt cupidatat minim fugiat sit exercitation ullamco occaecat est officia ut occaecat labore. Id consectetur cupidatat amet aute. Pariatur nostrud enim reprehenderit aliqua. Elit deserunt excepteur aute aliquip."\n\nconsole.print(\n    gradient_panel(\n        text,\n        title="Hello World",\n        title_align = \'center\',\n        subtitle = "The Cake is a Lie".\n        subtitle_align = \'right\'\n        num_of_gradients = 4,\n        justify = "left"\n        width = None\n    )\n)\n```\n![gradient_panel](static/gradient_panel.png)',
    'author': 'maxludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
