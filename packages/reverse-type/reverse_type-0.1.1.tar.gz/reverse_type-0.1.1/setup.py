# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['reverse-type = src.reverse_type:Main']}

setup_kwargs = {
    'name': 'reverse-type',
    'version': '0.1.1',
    'description': 'Embeds argument text in Unicode Right-To-Left and reverses it',
    'long_description': 'reverse-type\n============\n\nReverses the text given as command line arguments and embeds it in Unicode right-to-left marks\nsuch that in Unicode-aware environments it displays as specified.\n\nYou might use this in environments that do auto-censoring.\n',
    'author': 'Johnny Wezel',
    'author_email': 'j@wezel.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
