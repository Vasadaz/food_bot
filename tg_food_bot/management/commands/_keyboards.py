from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ._func_for_guest import get_guest_likes, get_guest

def start_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Принять', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def disagree_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Кнопка', callback_data='start')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def main_menu_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Рецепт', callback_data='recipe')],
        [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def profile_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Любимые рецепты', callback_data='liked_recipes')],
        [InlineKeyboardButton('Настройки', callback_data='settings')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def random_recipe_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Сохранить', callback_data='like'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Не показывать', callback_data='dislike')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def liked_random_recipe_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Сохранено. Удалить?', callback_data='unlike'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Не показывать', callback_data='dislike')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def liked_dishes_keyboard(chat_id):
    guest = get_guest(telegram_id=chat_id)
    dishes = get_guest_likes(guest)

    inline_keyboard = [
            [InlineKeyboardButton(f'{dish.title}', callback_data=f'{dish.title}')] for dish in dishes
    ]
    inline_keyboard.append([InlineKeyboardButton('Главное меню', callback_data='main_menu')])

    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def liked_dish_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Удалить', callback_data='delete'),
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def unliked_dish_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Сохранить', callback_data='save'),
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def categories_keyboard():
    '''Генератор кнопок с категориями для выбора'''
    inline_keyboard = [
        [InlineKeyboardButton('1', callback_data='category')],
        [InlineKeyboardButton('2', callback_data='category')],
        [InlineKeyboardButton('3', callback_data='category')],
        [InlineKeyboardButton('Сбросить категорию', callback_data='del_user_category'),
         InlineKeyboardButton('Главное меню', callback_data='main_menu')]
    ]

    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup

