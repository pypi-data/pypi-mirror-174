# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caiyun_tr']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['caiyun-tr = caiyun_tr.__main__:app']}

setup_kwargs = {
    'name': 'caiyun-tr',
    'version': '0.1.0',
    'description': 'caiyun_tr',
    'long_description': '# caiyun-tr\n[![pytest](https://github.com/ffreemt/caiyun-tr/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/caiyun-tr/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/caiyun_tr.svg)](https://badge.fury.io/py/caiyun_tr)\n\ncaiyun-tr\n\n## Install it\n\n```shell\npip install caiyun-tr --upgrade\n\n# pip install git+https://github.com/ffreemt/caiyun-tr\n# poetry add git+https://github.com/ffreemt/caiyun-tr\n# git clone https://github.com/ffreemt/caiyun-tr && cd caiyun-tr\n```\n\n## Use it\n```python\nfrom caiyun_tr import caiyun_tr\n\nprint(caiyun_tr("test this"))\n# 试试这个\n\n# only certain pairs are valid, en/ja is not valid\nprint(caiyun_tr("test this", from_lang="en", to_lang="ja"))\n# Exception: Unsupported trans_type (language pair)\n\n# zh/ja is valid\nprint(caiyun_tr("test this", from_lang="zh", to_lang="ja"))\n# テストして\n\nprint(caiyun_tr("テストして", \'ja\', "zh"))\n# 测试一下\n```\n\nOnly certain from_lang/to_lang pairs are supported by the website. There is nothing we can do about it.\n\nIf the caiyun website changes, this package will likely no longer work. If you feedback, the dev will try to fix it -- there is no guarantee thou. ',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/caiyun-tr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
