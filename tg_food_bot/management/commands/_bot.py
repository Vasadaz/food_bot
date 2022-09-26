from environs import Env
import logging

import redis

from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
)

from ._bot_functions import (
    start,
    input_user_name,
    input_phone_number,
    main_menu_handler,
    profile_handler,
    settings_handler,
    random_recipe_handler,
    liked_dishes,
    user_settings,
    liked_dish,
    save_phone,
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
        'PROFILE': profile_handler,
        'SETTINGS': settings_handler,
        'RANDOM_RECIPE': random_recipe_handler,
        'LIKED_DISHES': liked_dishes,
        'USER_SETTINGS': user_settings,
        'LIKED_DISH': liked_dish,
        'SAVE_PHONE': save_phone,

    }

    print(user_state)
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        error(user_state, err)


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
