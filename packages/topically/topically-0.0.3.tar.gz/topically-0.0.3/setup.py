# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topically', 'topically.prompts']

package_data = \
{'': ['*']}

install_requires = \
['cohere>=2.1,<3.0', 'pandas>=1.4,<2.0']

extras_require = \
{'bertopic': ['bertopic']}

setup_kwargs = {
    'name': 'topically',
    'version': '0.0.3',
    'description': '',
    'long_description': 'None',
    'author': 'Jay Alammar',
    'author_email': 'jay@cohere.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
