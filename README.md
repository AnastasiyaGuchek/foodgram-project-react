![Foodgram-project-react Workflow Status](https://github.com/AnastasiyaGuchek/foodgram-project-react/actions/workflows/main.yml/badge.svg)

Проект доступен по адресу 
http://84.201.138.18/recipes/


# Проект Foodgram
## Описание
Приложение, на котором пользователи будут публиковать свои рецепты, добавлять рецепты других пользователей в избранные и подписываться на публикации других авторов. Сервис «cписок покупок» позволит пользователям создавать список продуктов, которые необходимо приобрести для приготовления выбранных блюд. Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов.

## Стек технологий использованный в проекте:
- Python 3
- Django 2.2.28
- JWT
- DRF (Django REST framework)
- Django ORM
- Docker
- Gunicorn
- Nginx
- Яндекс Облако(Ubuntu 18.04)
- PostgreSQL

## Инструкции по развороту проекта
### Установить и запустить Docker
### Скачать данный репозиторий
### В директории infra создать файл env. и наполнить его по образцу ниже:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=qwerty # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
### Из директории infra/ выполнить команду docker-compose up -d --build
### После того как контейнеры nginx, db (БД PostgreSQL) и backend будут запущены, необходимо в контейнере backend создать и применить миграции, собрать статику, создать суперпользователя и загрузить данные с ингредиентами и тегами для создания рецептов. Для этого последовательно выполнить следующие команды:
```
sudo docker-compose exec web backend
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
python manage.py load_ingredients
```

## Автор в рамках учебного курса ЯП Python - разработчик бекенда:
[AnastasiyaGuchek](https://github.com/AnastasiyaGuchek)