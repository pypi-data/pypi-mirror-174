# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miller']

package_data = \
{'': ['*']}

install_requires = \
['amos>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'miller',
    'version': '0.1.3',
    'description': 'introspection tools using consistent, accessible syntax',
    'long_description': 'None',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
