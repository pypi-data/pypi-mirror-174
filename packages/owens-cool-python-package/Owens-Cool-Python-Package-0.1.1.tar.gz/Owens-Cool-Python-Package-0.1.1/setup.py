# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owens_cool_python_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'owens-cool-python-package',
    'version': '0.1.1',
    'description': 'My first python package, source code can be found on github',
    'long_description': None,
    'author': 'OwenSevenThousand',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
