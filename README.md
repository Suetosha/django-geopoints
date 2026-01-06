# GeoPoints API

Приложение для создания географических точек с возможностью оставлять сообщения и выполнять поиск точек и сообщений в
заданном радиусе.

Проект реализован на Django REST Framework с использованием PostGIS для геопоиска и JWT аутентификации.

## Описание проекта

Приложение предоставляет REST API для работы с географическими точками.
Пользователь может:

- зарегистрироваться и авторизоваться;
- создать точку на карте (широта и долгота);
- добавить сообщение к точке;
- выполнить поиск точек в заданном радиусе;
- выполнить поиск сообщений в заданном радиусе.

Доступ к основному функционалу ограничен JWT аутентификацией.

## Технологии

- Python 3.12
- Django 5.1.4
- Django REST Framework 3.15.2
- djangorestframework-simplejwt
- PostgreSQL + PostGIS (postgis/postgis:16-3.4-alpine)
- Docker, Docker Compose

## Запуск проекта

1. ### Клонирование репозитория
   ```bash
   git clone https://github.com/Suetosha/django-geopoints.git
   cd django-geopoints
   ```

2. ### Создание .env файла
   ```
   DJANGO_SECRET_KEY=your_secret_key
   
   DB_NAME=geopoints
   DB_USER=your_user 
   DB_PASSWORD=your_password
   DB_HOST=db
   DB_PORT=5432
   ```

3. ### Запуск контейнеров
   ```bash
   docker-compose up --build
   ```

4. ### Создание суперпользователя (Django Admin)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. ### Остановка проекта
   ```bash
   docker-compose down
   ```

## Аутентификация и авторизация

Аутентификация и авторизация выполняются с использованием JWT токенов.

Для доступа к защищённым эндпоинтам необходимо передавать access токен в HTTP заголовке:
```
Authorization: Bearer <access_token>
```
---
### Регистрация пользователя
**POST**
`/api/users/register/`

```bash
{
    "username": "test_user",
    "email": "test_user@example.com",
    "password": "test_password123"
}
```
---
### Логин и получение токена

**POST**
`/api/users/token/`


```bash
{
  "username": "test_user",
  "password": "test_password123"
}
```
---

### Создание точки

**POST**
`/api/points/`


Требуется JWT токен.


```bash
{
  "name": "Моя тестовая локация",
  "latitude": 45.03,
  "longitude": 38.97
}
```
---

### Создание сообщения к точке

**POST**
`/api/points/messages/`


Требуется JWT токен.
```bash
{
  "point": 1,
  "text": "Это тестовое сообщение в этой гео-точке."
}
```
---
### Поиск точек в радиусе

**GET**
`/api/points/search/?latitude=45.03&longitude=38.97&radius=1000`

Требуется JWT-токен.
---

### Поиск сообщений в радиусе

**GET**
`/api/messages/search/?latitude=45.03&longitude=38.97&radius=1000`

Требуется JWT-токен.

---

## Тестирование

### Через Postman

В проекте присутствует Postman-коллекция:

`Geopoints collection.postman_collection.json`

1. Импортируйте файл коллекции в Postman.
2. В настройках коллекции (вкладка Variables) установите значение http://localhost:8000.
3. Запустите готовые запросы с помощью кнопки Run.

### Через Django
  ```bash
docker-compose exec web python manage.py test
  ```
