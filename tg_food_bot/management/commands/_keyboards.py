from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
            InlineKeyboardButton('Лайк', callback_data='like'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Дизлайк', callback_data='dislike')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def liked_recipe_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Убрать из любимых', callback_data='unlike'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Дизлайк', callback_data='dislike')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


# def __():
#     return inline_kb_markup
#
#
# def __():
#     return inline_kb_markup