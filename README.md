# Кулинарный телеграм-бот
 
Проект food_bot поможет вам запустить своего телеграм-бота, 
который подберёт рецепты блюд по предпочтениям и бюджету.
Для блюд реализована система лайков и дизлайков, что гарантирует
сохранение любимых рецептов в личном кабинете и избавит ленту 
от не понравившихся блюд.

Возможности бота:
   - Просмотр рецептов
   - Добавление рецепта в список избранного
   - Просмотр списка избранного
   - Удаление рецепта из списка избранного
   - Удаление рецепта из списка выдачи

## Как установить

1. Клонировать репозиторий:

    ```shell
    git clone https://github.com/Vasadaz/food_bot.git
    ```

2. Установить зависимости:

    ```shell
    pip install -r requirements.txt
    ```

3. Создать файл `.env` с данными:

    ```dotenv
    ALLOWED_HOSTS=secure_host, myhost
    DEBUG=False
    REDIS_HOST=redis.host
    REDIS_PORT=redis.port
    REDIS_PASSWORD=redis.password
    TELEGRAM_TOKEN=telegram_bot_token
    ```

4. Если вы хотите использовать MySQL, тогда:

   - в файл `.env` добавить: 

      ```dotenv
      MYSQL_DB_NAME=mysql_db_name
      MYSQL_USER=mysql_user
      MYSQL_USER_PASSWORD=mysql_user_password
      MYSQL_HOST=mysql_db_host
      MYSQL_PORT=mysql_db_port
      ```

   - в файл `food_bot/settings.py` внести настройки для подключения к MySQL:

       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.mysql',
               'NAME': env.str('MYSQL_DB_NAME'),
               'HOST': env.str('MYSQL_HOST'),
               'PORT': env.str('MYSQL_PORT'),
               'USER': env.str('MYSQL_USER'),
               'PASSWORD': env.str('MYSQL_USER_PASSWORD'),
           }
       }
       ```

5. Сделать миграции:

    ```shell
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

6. Создать супер-пользователя для доступа к административной панели Django:

    ```shell
    python3 manage.py createsuperuser
    ```
   
7. Выполнить парсинг рецептов блюд с ресурса [povar.ru](https://povar.ru):
    
    ```shell
    python3 manage.py parse_recipes
    ```
   
    Все текстовые данные парсинга будут сохранены в JSON-файл `static/recipes.json`.
    Изображения к рецептам будут сохранены в директорию `media/images`.


8. Выполнить загрузку рецептов в БД из JSON-файла `static/recipes.json`:
    
    ```shell
    python3 manage.py upload_dishes
    ```
    
    Если возникнет необходимость удалить рецепты из БД, которые находятся в 
    JSON-файле `static/recipes.json`, то воспользуйтесь командой:

    ```shell 
    python3 manage.py delete_dishes
    ```

9. Для подтверждения обработки персональных данных сохранить файл pdf в директорию `static`
   под именем `Согласие на обработку персональных данных.pdf`.

   
10. Для доступа к административной панели Django используйте команду:
    
    ```shell
    python3 manage.py runserver
    ```
   
11. Для запуска телеграм-бота используйте команду:
    
    ```shell
    python3 manage.py start_bot
    ```
