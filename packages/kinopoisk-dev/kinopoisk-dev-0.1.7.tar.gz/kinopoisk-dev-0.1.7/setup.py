# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kinopoisk_dev', 'kinopoisk_dev.models', 'kinopoisk_dev.params']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'kinopoisk-dev',
    'version': '0.1.7',
    'description': 'Реализация Api для сервиса kinopoisk.dev',
    'long_description': '<div align="center">\n    <h1>Kinopoisk Dev Api</h1>\n    <p>Python-модуль для взаимодействия с неофициальным <a href="https://kinopoisk.dev/">API КиноПоиска</a></p>\n</div>\n\n### Установка\n\n```\n$ pip install kinopoisk-dev\n```\n\n### Получение токена\n\nДля получения токена необходимо перейти [kinopoisk.dev](https://kinopoisk.dev/documentation.html) и написать по\nконтактам.\n\n### Movie\n\nМетоды для работы с данными о фильмах\n\n#### Получить данные о фильме по Kinopoisk ID\n\nВозвращает информацию о фильме.\n\n* `Эндпоинт` - /movie\n* `Метод` - movie\n\n```python\nfrom kinopoisk_dev import KinopoiskDev, Field\n\nkp = KinopoiskDev(token=TOKEN)\nitem = kp.movie(field=Field.KP, search="301")\n```\n\n#### Сложная поисковая конструкция\n\nМожно задавать сложные конструкции для поиска.\n\n* `Эндпоинт` - /movie\n* `Метод` - movies\n\n##### Пример из [документации](https://kinopoisk.dev/documentation.html#%D0%BF%D0%BE%D0%B8%D1%81%D0%BA-get-5)\n\n> Представим что нам нужно найти сериалы typeNumber - 2 с рейтингом kp от 7 до 10 которые были выпущены с 2017 по 2020 год. При этом мы ходим чтобы они были осортированы по году в порядке возрастания, но при этом были отсортированы по голосам на imdb в порядке убывания. Для этого нам придется подготовить параметры\n\n```python\nfrom kinopoisk_dev import KinopoiskDev, Field, MovieParams\n\nkp = KinopoiskDev(token=TOKEN)\nitems = kp.movies([\n    MovieParams(field=\'rating.kp\', search=\'7-10\'),\n    MovieParams(field=Field.YEAR, search="2017-2020"),\n    MovieParams(field="typeNumber", search="2"),\n    MovieParams(sortField="year", sortType=1),\n    MovieParams(sortField="votes.imdb", sortType=-1),\n], limit=1000, page=1)\n```\n\n##### Получить информацию о списке фильмов\n\n```python\nfrom kinopoisk_dev import KinopoiskDev, Field, MovieParams\n\nkp = KinopoiskDev(token=TOKEN)\nitems = kp.movies([\n    MovieParams(field=\'id\', search=\'301\'),\n    MovieParams(field=Field.KP, search="326"),\n])\n```\n\n### Season\n\nМетоды для работы с сезонами сериалов\n\n#### Получить сезоны сериалы\n\nВозвращает информацию о сезонах\n\n- `Эндпоиск` - /season\n- `Метод` - season\n\n```python\nfrom kinopoisk_dev import KinopoiskDev, Field, SeasonParams\n\nkp = KinopoiskDev(token=TOKEN)\nseason = kp.season(field=Field.MOVIE_ID, search="1316601")\n```\n\n#### Получить сезоны списка сериалов\n\nВозвращает информацию о сезонах списка сериалов\n\n- `Эндпоиск` - /season\n- `Метод` - seasons\n\n```python\nfrom kinopoisk_dev import KinopoiskDev, Field, SeasonParams\n\nkp = KinopoiskDev(token=TOKEN)\nseasons = kp.seasons(params=[\n    SeasonParams(field=Field.MOVIE_ID, search="1316601"),\n    SeasonParams(field="movieId", search="4407805"),\n    SeasonParams(field=Field.MOVIE_ID, search="4476467"),\n    SeasonParams(field=Field.MOVIE_ID, search="4489470"),\n    SeasonParams(field=Field.MOVIE_ID, search="4670531"),\n    SeasonParams(field=Field.MOVIE_ID, search="571335"),\n], limit=1000, page=1, )\n```\n\n### Модели параметров\n\n#### MovieParams\n\nИмеет следующие поля\n\n| Поля       | Тип данных| Описание                             |\n| ---------- |:----------|:-------------------------------------|\n| field      | str/Field | Поле по которому происходит поиск    |\n| search     | str       | Данные по которым происходит поиск   |\n| sortField  | str       | По какому полю происходит сортировка |\n| sortType   | int       | В каком порядке выводить(1\\-1)       |\n\n### Заготовленные поля\n\n#### Field\n\n| Поля       | Значение   | Описание |\n| ---------- |:----------:| :-----|\n| KP            | id              | Поиск по id kinopoisk |\n| IMDB          | externalId.imdb | Поиск по id imdb |\n| TMDB          | externalId.tmdb | Поиск по id tmdb |\n| TYPE          | type | Поиск по типу |\n| NAME          | name | Поиск по имени |\n| YEAR          | year | Поиск по году |\n| TYPE_NUMBER   | typeNumber | Поиск по typeNumber |\n| MOVIE_ID      | movieId | Поиск по movieId |\n| LANGUAGE      | language | Поиск по языку |\n| STATUS        | status | Поиск по статусу |',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/odi1n/kinopoisk_dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
