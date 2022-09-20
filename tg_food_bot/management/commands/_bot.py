from environs import Env
import logging

from telegram.ext import Updater, CommandHandler



env = Env()
env.read_env()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(state, error):
    logger.warning(f'State {state} caused error {error}')


def start(update, context):
    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text='Привет, я работаю',
    )


def main():
    tg_token = env.str('TELEGRAM_TOKEN')

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()