from environs import Env
import logging

import redis
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler
)


env = Env()
env.read_env()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

_database = None

def error(state, error):
    logger.warning(f'State {state} caused error {error}')


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

def handle_users_reply(update, context):
    db = get_database_connection()

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id)

    states_functions = {
        'START': start,
        'INPUT_USER_NAME': input_user_name,
        'INPUT_PHONE_NUMBER': input_phone_number,
        'MAIN_MENU': main_menu_handler,
    }

    print(user_state)
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        error(user_state, err)


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


def main():
    tg_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()