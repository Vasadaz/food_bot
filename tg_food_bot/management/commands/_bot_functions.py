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
    elif query.data == 'disagree':
        message_text = 'Очень жаль, что вы не с нами. Если передумаете - введите /start'
        context.bot.send_message(
            chat_id=query.message.chat.id,
            text=message_text,
        )
        context.bot.delete_message(
            chat_id=update.message.chat.id,
            message_id=update.message.message_id
        )

    return 'INPUT_PHONE_NUMBER'


def input_phone_number(update, context):
    chat_id = update.message.chat_id

    context.bot.send_message(
        chat_id=chat_id,
        text='Введите номер телефона:',
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id - 1
    )

    return 'MAIN_MENU'


def main_menu_handler(update, context):
    chat_id = update.message.chat_id

    message_text = 'Выберите действие:'
    inline_keyboard = [
        [InlineKeyboardButton('Посмотреть рецепты', callback_data='recipes')],
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
        message_id=update.message.message_id - 1
    )