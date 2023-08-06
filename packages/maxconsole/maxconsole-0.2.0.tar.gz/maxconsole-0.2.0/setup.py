# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxconsole']
install_requires = \
['rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['get_console = maxconsole:get_console',
                     'maxconsole = maxconsole:main']}

setup_kwargs = {
    'name': 'maxconsole',
    'version': '0.2.0',
    'description': 'Themed Rich Conosle',
    'long_description': '# MaxConsole 0.1.0\n\nMaxConsole is a simple wrapper on top of Rich\'s Console class that allows you to easily create a console with a custom theme.\n\n## Installation\n\n### Pip\n\n```bash\npip install maxconsole\n```\n\n### Pipx (recommended)\n\n```bash\npipx install maxconsole\n```\n\n### Poetry\n\n```bash\npoetry add maxconsole\n```\n\n## Usage\n```python\nfrom maxconsole import get_console\n\nconsole = get_console() # It\'s that easy.\n```\n\n## Custimization\n\nMaking your own theme isn\'t hard but it\'s nice to have one spelled out for you, without lifting a finger.\n\n![maxconsole](maxconsole.svg)\n\n\n<hr />\n<div style="font-size:0.8em;color:#2e2e2e;background:#e2e2e2;padding:20px;border-radius:5px;">\n    <h3>MIT License</h3>\n    <p style="font-size:0.8em">Copyright (c) 2021 Max well Owen Ludden</p>\n    <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>\n    <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>\n    <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>\n</div>',
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
