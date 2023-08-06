# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_infer']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=6.5.0,<7.0.0',
 'dataclasses-json>=0.5.4,<0.6.0',
 'langid>=1.1.6,<2.0.0',
 'nltk>=3,<4',
 'numpy>=1.15,<2.0',
 'pandas>=1,<2',
 'python-dateutil>=2.1,<3.0',
 'scipy>=1,<2',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'type-infer',
    'version': '0.0.7',
    'description': 'Automated type inference for Machine Learning pipelines.',
    'long_description': '# MindsDB Type Infer\n<h1 align="center">\n\t<img width="300" src="https://github.com/mindsdb/mindsdb_native/blob/stable/assets/MindsDBColorPurp@3x.png?raw=true" alt="MindsDB">\n\t<br>\n\n</h1>\n<div align="center">\n\t<a href="https://github.com/mindsdb/type_infer/actions/workflows/python-package.yml"><img src="https://github.com/mindsdb/type_infer/actions/workflows/python-package.yml/badge.svg?branch=stable" alt="Type Infer workflow"></a>\n  <a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/badge/python-3.8.x|%203.9.x-brightgreen.svg" alt="Python supported"></a>\n  <a href="https://badge.fury.io/py/type-infer"><img src="https://badge.fury.io/py/type-infer.svg" alt="PyPI version" height="18"></a>\n<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/type-infer">  \n    <a href="https://join.slack.com/t/mindsdbcommunity/shared_invite/zt-o8mrmx3l-5ai~5H66s6wlxFfBMVI6wQ" target="_blank"><img src="https://img.shields.io/badge/slack-@mindsdbcommunity-brightgreen.svg?logo=slack " alt="MindsDB Community"></a>\n\t</br>\n\t\n  <h3 align="center">\n    <a href="https://www.mindsdb.com?utm_medium=community&utm_source=github&utm_campaign=mindsdb%20repo">Website</a>\n    <span> | </span>\n    <a href="https://mindsdb.github.io/type_infer/">Docs</a>\n    <span> | </span>\n    <a href="https://join.slack.com/t/mindsdbcommunity/shared_invite/zt-o8mrmx3l-5ai~5H66s6wlxFfBMVI6wQ">Community Slack</a>\n    <span> | </span>\n    <a href="https://github.com/mindsdb/mindsdb/projects">Contribute</a>\n    <span> | </span>\n    <a href="https://mindsdb.com/hacktoberfest">Hacktoberfest</a>\n  </h3>\n  \n</div>\nAutomated type inference for Machine Learning pipelines.\n\n# Documentation\n<a href="https://mindsdb.github.io/type_infer">Documentation link</a>\n',
    'author': 'MindsDB Inc.',
    'author_email': 'hello@mindsdb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
