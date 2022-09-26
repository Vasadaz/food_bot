import json
from environs import Env
import redis

from ._keyboards import (
    start_keyboard,
    disagree_keyboard,
    main_menu_keyboard,
    profile_keyboard,
    random_recipe_keyboard,
    liked_random_recipe_keyboard,
    liked_dishes_keyboard,
    categories_keyboard,
    liked_dish_keyboard,
    unliked_dish_keyboard,
    no_random_keyboard,
    budget_keyboard,
)

from ._func_for_dish import (
    get_random_dish,
    get_dish_content,
    get_dish,
)

from ._func_for_guest import (
    create_guest,
    get_guest,
    add_guest_name,
    add_guest_phonenumber,
    delete_guest,
    set_like,
    set_dislike,
    remove_like,
    get_guest_likes,
    remove_categories_of_guest,
    change_category_to_guest,
    change_budget,
    remove_budget,
)

env = Env()
env.read_env()
_database = None

def get_database_connection():
    global _database
    if _database is None:
        database_password = env.str("DATABASE_PASSWORD")
        database_host = env.str("DATABASE_HOST")
        database_port = env.str("DATABASE_PORT")
        _database = redis.Redis(
            host=database_host,
            port=database_port,
            password=database_password,
            decode_responses=True,
        )
    return _database
get_database_connection()


def start(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        message_id = query.message.message_id
    except:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    if not create_guest(chat_id):
        context.bot.send_message(
            chat_id=chat_id,
            text='Привет! Мы скучали :)',
            reply_markup=main_menu_keyboard()
        )
        return 'PROFILE'

    with open('static/Согласие на обработку персональных данных.pdf', 'rb') as file:
        context.bot.send_document(chat_id=chat_id, document=file)

    message_text = '''
Привет! Данный бот создан для того, чтобы разнообразить Ваше повседневное меню новыми блюдами. 
В нём Вы сможете просматривать случайные рецепты, выбрать категории интересующих Вас блюд и сохранить понравившеися.
Для начала работы с ботом нужно принять соглашение на обработку персональных данных.'''

    context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=start_keyboard()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )

    return 'INPUT_USER_NAME'


def input_user_name(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    if query.data == 'agree':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите ваше имя:',
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'INPUT_PHONE_NUMBER'

    elif query.data == 'disagree':
        message_text = 'Очень жаль, что Вы не с нами. Если передумаете - нажмите кнопку.'

        delete_guest(query.message.chat.id)
        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=disagree_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'START'


def input_phone_number(update, context):
    chat_id = update.message.chat_id

    guest = get_guest(chat_id)
    guest_name = update.message.text
    add_guest_name(guest, guest_name)

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона (пример: +79001234567):',
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id - 1
    )

    return 'SAVE_PHONE'


def save_phone(update, context):
    chat_id = update.message.chat_id
    guest = get_guest(chat_id)
    guest_phonenumber = update.message.text
    phonenumber_accepted = add_guest_phonenumber(guest, guest_phonenumber)

    if not phonenumber_accepted:
        context.bot.send_message(
            chat_id=chat_id,
            text='Неверный номер. Пожалуйста, введите номер в формате "+79990000000" или "9990000000"',
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=update.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=update.message.message_id - 1
        )
        return 'SAVE_PHONE'
    else:
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        return 'PROFILE'


def main_menu_handler(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        message_id = query.message.message_id
    except:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    message_text = 'Выберите действие:'

    context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=main_menu_keyboard()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id - 1
    )

    return 'PROFILE'


def profile_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    guest = get_guest(telegram_id=chat_id)
    guest_db = f'guest_tg_{chat_id}'

    if query.data == 'profile':
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=profile_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'SETTINGS'

    elif query.data == 'recipe':
        if not get_random_dish(guest):
            message = 'Нет блюд, соответствующих всем выбранным категориям.'
            context.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=no_random_keyboard()
            )
            context.bot.delete_message(
                chat_id=chat_id,
                message_id=query.message.message_id
            )
            return 'SETTINGS'

        dish = get_random_dish(guest)
        dish_content = get_dish_content(dish)

        _database.set(
            guest_db,
            json.dumps({
                'dish': dish.title,
            })
        )

        context.bot.send_photo(
            chat_id=chat_id,
            photo=dish_content['image']
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=dish_content['message'],
            reply_markup=random_recipe_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'RANDOM_RECIPE'


def settings_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    guest = get_guest(telegram_id=chat_id)

    if query.data == 'liked_recipes':
        if get_guest_likes(guest):
            message_text = 'Любимые рецепты:'
        else:
            message_text = 'У вас нет любимых рецептов.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=liked_dishes_keyboard(chat_id)
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'LIKED_DISHES'

    elif query.data == 'settings':
        message_text = f'Выберите интересующие Вас категории блюд'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=categories_keyboard(chat_id)
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'USER_SETTINGS'

    elif query.data == 'budget':
        message_text = 'Выберите максимальную стоимость порции.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=budget_keyboard(chat_id)
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'BUDGET'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'PROFILE'


def random_recipe_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    guest = get_guest(telegram_id=chat_id)
    guest_db = f'guest_tg_{chat_id}'

    if query.data == 'like':
        dish_title = json.loads(_database.get(guest_db))['dish']
        dish = get_dish(dish_title)
        set_like(guest, dish)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=liked_random_recipe_keyboard()
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'unlike':
        dish_title = json.loads(_database.get(guest_db))['dish']
        dish = get_dish(dish_title)
        remove_like(guest, dish)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=random_recipe_keyboard()
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'dislike':
        dish_title = json.loads(_database.get(guest_db))['dish']
        dish = get_dish(dish_title)
        set_dislike(guest, dish)

        if not get_random_dish(guest):
            message = 'Нет блюд, соответствующих всем выбранным категориям'
            context.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=no_random_keyboard()
            )
            context.bot.delete_message(
                chat_id=chat_id,
                message_id=query.message.message_id
            )
            return 'SETTINGS'

        dish = get_random_dish(guest)
        dish_content = get_dish_content(dish)
        _database.set(
            guest_db,
            json.dumps({
                'dish': dish.title,
            })
        )

        context.bot.send_photo(
            chat_id=chat_id,
            photo=dish_content['image']
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=dish_content['message'],
            reply_markup=random_recipe_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'next':
        dish = get_random_dish(guest)
        dish_content = get_dish_content(dish)
        _database.set(
            guest_db,
            json.dumps({
                'dish': dish.title,
            })
        )

        context.bot.send_photo(
            chat_id=chat_id,
            photo=dish_content['image']
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=dish_content['message'],
            reply_markup=random_recipe_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'PROFILE'


def liked_dishes(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    if query.data == 'main_menu':
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

    else :
        guest_db = f'guest_tg_{chat_id}'
        dish_title = str(query.data)
        _database.set(
            guest_db,
            json.dumps({
                'dish': dish_title,
            })
        )

        dish = get_dish(dish_title)
        dish_content = get_dish_content(dish)

        context.bot.send_photo(
            chat_id=chat_id,
            photo=dish_content['image']
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=dish_content['message'],
            reply_markup=liked_dish_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'LIKED_DISH'


def liked_dish(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    guest = get_guest(telegram_id=chat_id)
    guest_db = f'guest_tg_{chat_id}'

    if query.data == 'main_menu':
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id - 1
        )
        return 'PROFILE'

    elif query.data == 'delete':
        dish_title = json.loads(_database.get(guest_db))['dish']
        dish = get_dish(dish_title)
        remove_like(guest, dish)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=unliked_dish_keyboard()
        )
        return 'LIKED_DISH'

    elif query.data == 'save':
        dish_title = json.loads(_database.get(guest_db))['dish']
        dish = get_dish(dish_title)
        set_like(guest, dish)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=liked_dish_keyboard()
        )
        return 'LIKED_DISH'


def user_settings(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    guest = get_guest(telegram_id=chat_id)

    if query.data == 'main_menu':
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

    elif query.data == 'del_user_categories':
        remove_categories_of_guest(guest)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=categories_keyboard(chat_id)
        )
        return 'USER_SETTINGS'

    else:
        category_title = query.data
        change_category_to_guest(guest, category_title)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=categories_keyboard(chat_id)
        )
        return 'USER_SETTINGS'


def user_budget_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    guest = get_guest(telegram_id=chat_id)

    if query.data == 'main_menu':
        message_text = 'Добро пожаловать в главное меню.'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

    elif query.data == 'del_user_budget':
        remove_budget(guest)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=budget_keyboard(chat_id)
        )
        return 'BUDGET'

    else:
        budget = query.data
        change_budget(guest, budget)

        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=budget_keyboard(chat_id)
        )
        return 'BUDGET'
