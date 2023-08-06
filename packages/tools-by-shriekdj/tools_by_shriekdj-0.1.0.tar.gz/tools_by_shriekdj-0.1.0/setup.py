# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tools_by_shriekdj']

package_data = \
{'': ['*']}

install_requires = \
['phonenumbers>=8.12.57,<9.0.0']

setup_kwargs = {
    'name': 'tools-by-shriekdj',
    'version': '0.1.0',
    'description': '',
    'long_description': '# tools_by_shriekdj\n\nYou Can Use this package for cleaning address and retrieving url, emails, phonenumbers and removing duplicates\n\n## Steps\n\n> Just Install This package by `pip install tools_by_shriekdj`\n\n### How to use\n\n```python\nimport tools_by_shriekdj as dj\n\ndj.retrieve_phone_numbers("Call me at 1800-202-2022 if it\'s before 9:30, or on 703-4800500 after 10am.")\n\n>>> [\'18002022022\', \'7034800500\']\n```\n\n',
    'author': 'Shrikant Dhayje',
    'author_email': 'shrikantdhayaje@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
