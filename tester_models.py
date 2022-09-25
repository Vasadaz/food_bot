import os
import django
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_bot.settings')
django.setup()


from tg_food_bot.management.commands._func_for_category import (
    get_categories,
)

from tg_food_bot.management.commands._func_for_guest import (
    add_guest,
    add_guest_phonenumber,
    add_categories_to_guest,
    get_guest,
    add_new_categories_to_guest,
    normalize_owners_phonenumber,
    remove_categories_of_guest,
    remove_dislike,
    remove_like,
    set_dislike,
    set_like,
)

from tg_food_bot.management.commands._func_for_dish import (
    get_random_dish,
    get_dish_content,
)

name = random.choice(['Иван', 'Петя', 'Юля','Игнат', 'Саша', 'Марина'])
telegram_id = random.randrange(10000000)


guest_data = {
    "name": f'{name} {telegram_id}',
    'telegram_id': telegram_id,
    'phonenumber': '45445678'
}

print(f'Запрос всех категорий:\n {get_categories() = }\n')
categories = get_categories()

print(f'Добавление гостя(если номер неликвидный, то поле phonenumber = None):\n {add_guest(guest_data) = }\n')
guest = get_guest(guest_data['telegram_id'])

print(f'{guest_data["name"]} - Проверка ликвидности номера:\n {normalize_owners_phonenumber("+7901234567") = }\n')
print(f'{guest_data["name"]} - Проверка ликвидности номера:\n {normalize_owners_phonenumber("01234567") = }\n')
print(f'{guest_data["name"]} - Проверка ликвидности номера:\n {normalize_owners_phonenumber("+79012345678") = }\n')
print(f'{guest_data["name"]} - Проверка ликвидности номера:\n {normalize_owners_phonenumber("9012345678") = }\n')
print(f'{guest_data["name"]} - Проверка ликвидности номера:\n {normalize_owners_phonenumber("89012345678") = }\n')

print(f'{guest_data["name"]} - Добавление номера гостю:\n {add_guest_phonenumber(guest, "89876543210") = }\n')

print(f'{guest_data["name"]} - Получить гостя:\n {get_guest(guest_data["telegram_id"]) = }\n')

select_categories = [random.choice(categories)]
print(f'{guest_data["name"]} - Добавить категории {select_categories} для гостя:\n '
      f'{add_categories_to_guest(guest, select_categories) = }\n')

select_new_categories = random.choices(categories, k=2)
print(f'{guest_data["name"]} - Установить новые категории {select_new_categories} для гостя:\n '
      f'{ add_new_categories_to_guest(guest, select_new_categories) = }\n')

print(f'{guest_data["name"]} - Удалить все категории у гостя:\n { remove_categories_of_guest(guest) = }\n')

select_categories = random.choices(categories, k=2)
print(f'{guest_data["name"]} - Добавить категории {select_categories} для гостя:\n '
      f'{add_categories_to_guest(guest, select_categories) = }\n')

print(f'{guest_data["name"]} - Получить случайное блюдо по выбранным категориям (блюда из likes и dislikes исключаются):\n '
      f'{ get_random_dish(guest) = }\n')

dish_1 = get_random_dish(guest)
dish_2 = get_random_dish(guest)
dish_3 = get_random_dish(guest)
print(f'{guest_data["name"]} - Поставить лайк блюду {dish_1 = }:\n { set_like(guest, dish_1) = }\n')
print(f'{guest_data["name"]} - Поставить лайк блюду {dish_2 = }:\n { set_like(guest, dish_2) = }\n')
print(f'{guest_data["name"]} - Поставить лайк блюду {dish_3 = }:\n { set_like(guest, dish_3) = }\n')

dish_4 = get_random_dish(guest)
dish_5 = get_random_dish(guest)
dish_6 = get_random_dish(guest)
print(f'{guest_data["name"]} - Поставить дизлайк блюду {dish_4 = }:\n { set_dislike(guest, dish_4) = }\n')
print(f'{guest_data["name"]} - Поставить дизлайк блюду {dish_5 = }:\n { set_dislike(guest, dish_5) = }\n')
print(f'{guest_data["name"]} - Поставить дизлайк блюду {dish_6 = }:\n { set_dislike(guest, dish_6) = }\n')

print(f'{guest_data["name"]} - Поставить лайк блюду {dish_4 = }, которое уже было дизлайкнуто(он удалиться из '
      f'dislikes и добавится в likes):\n '
      f'{ set_like(guest, dish_4) = }\n')
print(f'{guest_data["name"]} - Поставить дизлайк блюду {dish_1 = }, которое уже было лайкнуто(он удалиться из likes и '
      f'добавится в dislikes):\n '
      f'{ set_dislike(guest, dish_1) = }\n')

print(f'{guest_data["name"]} - Убрать лайк блюду {dish_2 = }:\n { remove_like(guest, dish_2) = }\n')
print(f'{guest_data["name"]} - Убрать дизлайк блюду {dish_5 = }:\n { remove_dislike(guest, dish_5) = }\n')
