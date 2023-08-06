# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibis_substrait',
 'ibis_substrait.compiler',
 'ibis_substrait.proto',
 'ibis_substrait.proto.substrait',
 'ibis_substrait.proto.substrait.ibis',
 'ibis_substrait.proto.substrait.ibis.extensions',
 'ibis_substrait.tests',
 'ibis_substrait.tests.compiler']

package_data = \
{'': ['*']}

install_requires = \
['protobuf==3.20.1', 'sqlalchemy>=1,<2']

extras_require = \
{':python_version >= "3.8" and python_version < "3.11"': ['ibis-framework>=3,<4'],
 ':python_version >= "3.8" and python_version < "4"': ['ibis-framework']}

setup_kwargs = {
    'name': 'ibis-substrait',
    'version': '2.14.1',
    'description': 'Subtrait compiler for ibis',
    'long_description': "# [Ibis](https://ibis-project.org) + [Substrait](https://substrait.io)\n\nThis repo houses the Substrait compiler for ibis.\n\nWe're just getting started here, so stay tuned!\n",
    'author': 'Ibis Contributors',
    'author_email': 'None',
    'maintainer': 'Ibis Contributors',
    'maintainer_email': 'None',
    'url': 'https://github.com/ibis-project/ibis-substrait',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
