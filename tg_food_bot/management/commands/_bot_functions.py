from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start(update, context):
    chat_id = update.message.chat.id

    inline_keyboard = [
        [InlineKeyboardButton('Принять', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    context.bot.send_message(
        chat_id=chat_id,
        text='Привет! Для начала работы с ботом нужно принять соглашение на обработку персональных данных',
        reply_markup=inline_markup
    )
    context.bot.send_document(
        chat_id=chat_id,
        document='https://www.africau.edu/images/default/sample.pdf'
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
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
        message_text = 'Очень жаль, что вы не с нами. Если передумаете - введите /start'
        context.bot.send_message(
            chat_id=query.message.chat.id,
            text=message_text,
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
    except:
        chat_id = update.message.chat_id

    message_text = 'Выберите действие:'
    inline_keyboard = [
        [InlineKeyboardButton('Рецепт', callback_data='recipe')],
        [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        reply_markup=inline_kb_markup
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id - 1
    )

    return 'PROFILE'


def profile_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'profile':
        message_text = 'Выберите действие:'
        inline_keyboard = [
            [InlineKeyboardButton('Любимые рецепты', callback_data='liked_recipes')],
            [InlineKeyboardButton('Настройки', callback_data='settings')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'SETTINGS'

    elif query.data == 'recipe':
        message_text = 'Тут будет рецепт'

        inline_keyboard = [
            [
                InlineKeyboardButton('Лайк', callback_data='like'),
                InlineKeyboardButton('Следующий', callback_data='next'),
                InlineKeyboardButton('Дизлайк', callback_data='dislike')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
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
        inline_keyboard = [
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'LIKED_DISHES'

    elif query.data == 'settings':
        message_text = 'Настройка фильтров отображения рецептов:' \
                       'Генератор кнопок по категориям + сброс всех '
        inline_keyboard = [
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'USER_SETTINGS'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'
        inline_keyboard = [
            [InlineKeyboardButton('Рецепт', callback_data='recipe')],
            [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'


def random_recipe_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'like':
        message_text = 'Рецепт добавлен в "Любимые"'

        inline_keyboard = [
            [
                InlineKeyboardButton('Убрать из любимых', callback_data='unlike'),
                InlineKeyboardButton('Следующий', callback_data='next'),
                InlineKeyboardButton('Дизлайк', callback_data='dislike')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'dislike':
        message_text = 'Рецепт убран из выдачи, попробуйте этот рецепт (реализовать отображение нового рецепта)'

        inline_keyboard = [
            [
                InlineKeyboardButton('Лайк', callback_data='like'),
                InlineKeyboardButton('Следующий', callback_data='next'),
                InlineKeyboardButton('Дизлайк', callback_data='dislike')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'next':
        message_text = 'Новый рецепт (реализовать отображение нового рецепта)'

        inline_keyboard = [
            [
                InlineKeyboardButton('Лайк', callback_data='like'),
                InlineKeyboardButton('Следующий', callback_data='next'),
                InlineKeyboardButton('Дизлайк', callback_data='dislike')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'unlike':
        message_text = 'Рецепт добавлен в "Любимые"'

        inline_keyboard = [
            [
                InlineKeyboardButton('Лайк', callback_data='like'),
                InlineKeyboardButton('Следующий', callback_data='next'),
                InlineKeyboardButton('Дизлайк', callback_data='dislike')],
            [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        return 'RANDOM_RECIPE'

    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'
        inline_keyboard = [
            [InlineKeyboardButton('Рецепт', callback_data='recipe')],
            [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        return 'PROFILE'


def liked_dishes(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'liked':
        pass
    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'
        inline_keyboard = [
            [InlineKeyboardButton('Рецепт', callback_data='recipe')],
            [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'

def user_settings(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id

    if query.data == 'filtres':
        pass
    elif query.data == 'main_menu':
        message_text = 'Выберите действие:'
        inline_keyboard = [
            [InlineKeyboardButton('Рецепт', callback_data='recipe')],
            [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
        ]
        inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

        context.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=inline_kb_markup
        )
        context.bot.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        return 'PROFILE'