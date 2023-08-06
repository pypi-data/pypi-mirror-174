# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_connection']

package_data = \
{'': ['*']}

install_requires = \
['fastapi<1.0.0', 'pydantic>=1.0.0,<2.0.0', 'websockets>=10.0.0,<11.0.0']

setup_kwargs = {
    'name': 'data-connection',
    'version': '0.0.3',
    'description': 'Передача данных между сервисами',
    'long_description': '# data_exchange\n\n## Описание\n\nОбмен данными между микросервисами\n\n- signal - элементарный тип данных. Кроме значения, хранит также время последнего чтения / записи, код качества, единицу измерения, пределы измерения.\n\n- channel - объект для связи signal с периферийными значениями.\n\n- driver - управляет объектами channel.\n\n- datapoint - объект для храненения данных. Связывает signal и channel.\n\n## Разработка\n\nУстановить виртуальное окружение\n\n```sh\npoetry install\n```\n\nСобрать пакет\n\n```sh\npoetry build\n```\n\nОпубликовать пакет\n\n```sh\npoetry publish --username Konstantin.Dudersky@gmail.com --password __TOKEN__\n```\n',
    'author': 'konstantin-dudersky',
    'author_email': 'konstantin.dudersky@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Konstantin-Dudersky/data_exchange.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
