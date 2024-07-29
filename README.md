# api_yamdb

## Описание проекта

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Задача

Проект решает задачу предоставления доступа к сервису направленному на сбор отзывов о произведениях через REST API. Это позволяет разработчикам легко интегрировать возможности YaMDb в свои приложения, создавать мобильные клиенты и расширять функционал веб-приложения.

## Технологический стек

Для разработки этого проекта использовались следующие технологии:

- **Python**: Основной язык программирования для бизнес-логики и взаимодействия с базой данных.
- **Django**: Python-фреймворк для разработки веб-приложений.
- **SQLite**: Встроенная реляционная база данных, используемая в качестве хранилища данных проекта.
- **RESTful API**: Проектирование и разработка API с учетом принципов REST для обеспечения эффективного взаимодействия клиентов с сервером.


## Развертывание проекта
Клонируем репозиторий и переходим в него в командной строке:

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

В проекте реализована функция для базового заполнение базы данных:

```
python manage.py load_data
```

## Примеры запросов к API
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
Ответ:
```
{
"email": "string",
"username": "string"
}
```

```
http://127.0.0.1:8000/api/v1/titles/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Ответ:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

## Автор: Подзоров Михаил, Дмитрий Шувалов, Алексей Рябинин