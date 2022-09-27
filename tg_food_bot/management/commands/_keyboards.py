from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ._func_for_guest import get_guest_likes, get_guest, get_guest_categories
from ._func_for_category import get_categories


def start_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Принять', callback_data='agree')],
        [InlineKeyboardButton('Отказаться', callback_data='disagree')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def disagree_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Вернуться', callback_data='start')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def main_menu_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Случайный рецепт', callback_data='recipe')],
        [InlineKeyboardButton('Личный кабинет', callback_data='profile')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def profile_keyboard():
    inline_keyboard = [
        [InlineKeyboardButton('Любимые рецепты', callback_data='liked_recipes')],
        [InlineKeyboardButton('Выбор категорий', callback_data='settings')],
        [InlineKeyboardButton('Выбор бюджета', callback_data='budget')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def random_recipe_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Сохранить', callback_data='like'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Скрыть \U0000274C', callback_data='dislike')],
        [InlineKeyboardButton('Главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def liked_random_recipe_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Сохранено. \U00002705', callback_data='unlike'),
            InlineKeyboardButton('Следующий', callback_data='next'),
            InlineKeyboardButton('Скрыть \U0000274C', callback_data='dislike')],
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
            InlineKeyboardButton('Удалить \U0000274C', callback_data='delete'),
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


def categories_keyboard(chat_id):
    guest = get_guest(telegram_id=chat_id)
    guest_categories = [category.title for category in get_guest_categories(guest)]
    categories = get_categories()
    inline_keyboard = []
    for category in categories:
        if category in guest_categories:
            inline_keyboard.append([InlineKeyboardButton(f'{category} \U00002705', callback_data=f'{category}')])
        else:
            inline_keyboard.append([InlineKeyboardButton(f'{category}', callback_data=f'{category}')])

    inline_keyboard.append(
        [InlineKeyboardButton('Сбросить', callback_data='del_user_categories'),
         InlineKeyboardButton('Главное меню', callback_data='main_menu')]
    )

    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def no_random_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Выбор категорий', callback_data='settings'),
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup


def budget_keyboard(chat_id):
    guest = get_guest(telegram_id=chat_id)
    if guest.budget:
        guest_budget = guest.budget
    else:
        guest_budget = None
    budgets = [200, 350, 500, 750, 1000]

    inline_keyboard = []
    for budget in budgets:
        if budget == guest_budget:
            inline_keyboard.append([InlineKeyboardButton(f'{budget} \U00002705', callback_data=budget)])
        else:
            inline_keyboard.append([InlineKeyboardButton(f'{budget}', callback_data=budget)])

    inline_keyboard.append(
        [
            InlineKeyboardButton('Сбросить', callback_data='del_user_budget'),
            InlineKeyboardButton('Главное меню', callback_data='main_menu')
        ]
    )

    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)
    return inline_kb_markup
