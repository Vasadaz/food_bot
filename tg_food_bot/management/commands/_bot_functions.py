from ._func_for_dish import (
    get_random_dish,
    get_dish_content
)

from ._keyboards import (
    start_keyboard,
    disagree_keyboard,
    main_menu_keyboard,
    profile_keyboard,
    random_recipe_keyboard,
    liked_random_recipe_keyboard,
    liked_dishes_keyboard,
    categories_keyboard,
    liked_dish_keyboard
)

def start(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        message_id = query.message.message_id
    except:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Привет! Для начала работы с ботом нужно принять соглашение на обработку персональных данных',
        reply_markup=start_keyboard()
    )
    context.bot.send_document(
        chat_id=chat_id,
        document='https://www.africau.edu/images/default/sample.pdf'
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )

    return 'INPUT_USER_NAME'


def input_user_name(update, context):
    query = update.callback_query

    if query.data == 'agree':
        context.bot.send_message(
            chat_id=query.message.chat.id,
            text='Введите ваше имя:',
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id + 1
        )
        return 'INPUT_PHONE_NUMBER'

    elif query.data == 'disagree':
        message_text = 'Очень жаль, что вы не с нами. Если передумаете - нажмите кнопку'

        context.bot.send_message(
            chat_id=query.message.chat.id,
            text=message_text,
            reply_markup=disagree_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id + 1
        )
        return 'START'


def input_phone_number(update, context):
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона:',
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id - 1
    )

    return 'MAIN_MENU'


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

    if query.data == 'profile':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=profile_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'SETTINGS'

    elif query.data == 'recipe':
        dish = get_random_dish()
        dish_content = get_dish_content(dish)

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
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'RANDOM_RECIPE'


def settings_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'liked_recipes':
        message_text = 'Список кнопок с любимыми рецептами,' \
                       ' либо "извините, у вас нет любимых рецептов"(генератор кнопок)'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=liked_dishes_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'LIKED_DISHES'

    elif query.data == 'settings':
        message_text = 'Настройка фильтров отображения рецептов:' \
                       'Генератор кнопок по категориям + сброс всех '

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=categories_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'USER_SETTINGS'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'


def random_recipe_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if query.data == 'like':
        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=liked_random_recipe_keyboard()
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'unlike':
        context.bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=random_recipe_keyboard()
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'dislike':
        dish = get_random_dish()
        dish_content = get_dish_content(dish)

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
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id - 1
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'next':
        dish = get_random_dish()
        dish_content = get_dish_content(dish)

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
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
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
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id - 1
        )
        return 'PROFILE'


def liked_dishes(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'liked':
        message_text = 'Cписок любимых блюд'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=liked_dish_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'LIKED_DISHES'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'


def user_settings(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'category':
        message_text = 'Категории блюд. Сейчас выбрана категория {category}'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=categories_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'USER_CATEGORIES'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'


def user_dishes(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

    elif query.data == 'dish':
        message_text = 'Блюдо'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=liked_dish_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return


def user_categories(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'main_menu':
        message_text = 'Выберите действие:'

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=main_menu_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

    elif query.data == 'category':
        message_text = 'Категории блюд. Сейчас выбрана категория {category}'

        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text=message_text,
            reply_markup=categories_keyboard()
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'USER_CATEGORIES'
