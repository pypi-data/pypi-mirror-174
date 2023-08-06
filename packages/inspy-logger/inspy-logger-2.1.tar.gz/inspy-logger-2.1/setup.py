# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspy_logger', 'inspy_logger.errors', 'inspy_logger.helpers']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'colorama>=0.4.6,<0.5.0',
 'colorlog>=6.7,<7.0',
 'domain-suffixes>=1.1.3,<2.0.0',
 'humanize>=4.4.0,<5.0.0',
 'luddite>=1.0.1,<2.0.0',
 'packaging>=21.0,<22.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools-autover>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'inspy-logger',
    'version': '2.1',
    'description': 'Colorable, scalable logger for CLI',
    'long_description': None,
    'author': 'Taylor-Jayde Blackstone',
    'author_email': 'tayjaybabee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
