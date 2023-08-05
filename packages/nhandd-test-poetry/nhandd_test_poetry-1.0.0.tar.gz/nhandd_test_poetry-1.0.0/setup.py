# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nhandd_test_poetry']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9', 'termcolor>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'nhandd-test-poetry',
    'version': '1.0.0',
    'description': '',
    'long_description': '',
    'author': 'NhanDD',
    'author_email': 'hp.duongducnhan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
