# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiovkapi',
 'aiovkapi.types',
 'aiovkapi.types.methods',
 'aiovkapi.types.responses']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.0', 'aiohttp>=3.0,<4.0', 'pydantic>=1.0,<2.0']

setup_kwargs = {
    'name': 'aiovkapi',
    'version': '0.1.1',
    'description': 'Библиотека для VK API с мимикрией под приложения VK',
    'long_description': '# AIOVKAPI\n\n![](https://img.shields.io/github/license/FBHTeam/aiovkapi)\n\nБиблиотека для VK API с мимикрией под приложения VK\n\n\n## Полезные ссылки\n[Документация](https://github.com/FBHTeam/aiovkapi/tree/master/docs/index.md)',
    'author': 'lordralinc',
    'author_email': '46781434+lordralinc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FBHTeam/aiovkapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
