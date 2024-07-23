# api_yamdb

## Автор: Подзоров Михаил, Дмитрий Шувалов, Алексей Рябинин

## Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Задача

Проект решает задачу предоставления доступа к сервису направленному на сбор отзывов о произведениях через REST API. Это позволяет разработчикам легко интегрировать возможности YaMDb в свои приложения, создавать мобильные клиенты и расширять функционал веб-приложения.

## Примеры запросов к API
```
admin/
api/v1/ ^categories/$ [name='categories-list']
api/v1/ ^categories\.(?P<format>[a-z0-9]+)/?$ [name='categories-list']
api/v1/ ^categories/(?P<pk>[^/.]+)/$ [name='categories-detail']
api/v1/ ^categories/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='categories-detail']
api/v1/ ^genres/$ [name='genres-list']
api/v1/ ^genres\.(?P<format>[a-z0-9]+)/?$ [name='genres-list']
api/v1/ ^genres/(?P<pk>[^/.]+)/$ [name='genres-detail']
api/v1/ ^genres/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='genres-detail']
api/v1/ ^titles/$ [name='titles-list']
api/v1/ ^titles\.(?P<format>[a-z0-9]+)/?$ [name='titles-list']
api/v1/ ^titles/(?P<pk>[^/.]+)/$ [name='titles-detail']
api/v1/ ^titles/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='titles-detail']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/$ [name='review-list']
api/v1/ ^titles/(?P<title_id>\d+)/reviews\.(?P<format>[a-z0-9]+)/?$ [name='review-list']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<pk>[^/.]+)/$ [name='review-detail']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='review-detail']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/$ [name='comment-list']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments\.(?P<format>[a-z0-9]+)/?$ [name='comment-list']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<pk>[^/.]+)/$ [name='comment-detail']
api/v1/ ^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='comment-detail']
api/v1/ ^$ [name='api-root']
api/v1/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
redoc/ [name='redoc']
```
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Resurection1/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Технологический стек

Для разработки этого проекта использовались следующие технологии:

- **Python**: Основной язык программирования для бизнес-логики и взаимодействия с базой данных.
- **Django**: Python-фреймворк для разработки веб-приложений.
- **SQLite**: Встроенная реляционная база данных, используемая в качестве хранилища данных проекта.
- **RESTful API**: Проектирование и разработка API с учетом принципов REST для обеспечения эффективного взаимодействия клиентов с сервером.