# food_bot
 
С помощью бота вы можете разнообразить ваше меню.

Возможности бота:
- Просмотр рецептов
- Добавление рецепта в список избранного
- Просмотр списка избранного
- Удаление рецепта из списка избранного
- Удаление рецепта из списка выдачи

## Как установить

1. Клонировать репозиторий:

```commandline
git clone https://github.com/HardRope/food_bot.git
```

 2. Установить зависимости:

```commandline
pip install -r requirements.txt
```

 3. Сделать миграции:

```commandline
python3 manage.py makemigrations
python3 manage.py migrate
```

 4. Создать файл `.env` с данными:

```commandline
TELEGRAM_TOKEN=telegram_bot_token
DATABASE_HOST=redis.host
DATABASE_PORT=redis.port
DATABASE_PASSWORD=redis.password
```

 5. Создать супер-пользователя для доступа в админку Django:

```commandline
python3 manage.py createsuperuser
```
