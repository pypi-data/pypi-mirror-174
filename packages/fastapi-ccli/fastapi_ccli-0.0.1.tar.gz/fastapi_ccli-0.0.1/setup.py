# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_ccli',
 'fastapi_ccli.cloner',
 'fastapi_ccli.cloner.en',
 'fastapi_ccli.cloner.zh',
 'fastapi_ccli.utils']

package_data = \
{'': ['*']}

install_requires = \
['keyboard==0.13.5',
 'questionary==1.10.0',
 'requests==2.25.1',
 'typer[all]==0.6.1']

entry_points = \
{'console_scripts': ['fastapi-ccli = fastapi_ccli.main:main']}

setup_kwargs = {
    'name': 'fastapi-ccli',
    'version': '0.0.1',
    'description': 'Tool to automatically clone existing fastapi repositories based on command line conditions',
    'long_description': '# FastAPI Project Clone CLI\n\n> 此程序使用 [Typer](https://typer.tiangolo.com/) 创建\n\n## 使用\n\npip 安装：\n\n```shell\npip install fastapi-ccli\n```\n\n查看使用帮助\n\n```shell\nfastapi-ccli --help\n```\n',
    'author': 'wu',
    'author_email': 'jianhengwu0407@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wu-clan/fastapi_ccli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
