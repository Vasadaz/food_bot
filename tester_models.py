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
    'name': f'{name} {telegram_id}',
    'telegram_id': telegram_id,
    'phonenumber': '45445678'
}

print(f'Запрос всех категорий:\n {get_categories() = }\n')
categories = get_categories()

print(f'Добавление гостя(если номер неликвидный, то поле phonenumber = None):\n {add_guest(guest_data) = }\n')
guest = get_guest(guest_data['telegram_id'])

print(f'Проверка ликвидности номера:\n {normalize_owners_phonenumber("+7901234567") = }\n')
print(f'Проверка ликвидности номера:\n {normalize_owners_phonenumber("01234567") = }\n')
print(f'Проверка ликвидности номера:\n {normalize_owners_phonenumber("+79012345678") = }\n')
print(f'Проверка ликвидности номера:\n {normalize_owners_phonenumber("9012345678") = }\n')
print(f'Проверка ликвидности номера:\n {normalize_owners_phonenumber("89012345678") = }\n')

print(f'Добавление номера гостю:\n {add_guest_phonenumber(guest, "89876543210") = }\n')

print(f'Получить гостя:\n {get_guest(guest_data["telegram_id"]) = }\n')

select_categories = [random.choice(categories)]
print(f'Добавить категории {select_categories} для гостя:\n {add_categories_to_guest(guest, select_categories) = }\n')

select_new_categories = random.choices(categories, k=2)
print(f'Установить новые категории {select_new_categories} для гостя:\n { add_new_categories_to_guest(guest, select_new_categories) = }\n')

#print(f'Удалить все категории у гостя:\n { remove_categories_of_guest(guest) = }\n')

print(f'Получить случайное блюдо согласно предпочтениям и лайкам гостя:\n { get_random_dish(guest) = }\n')

'''
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
print(f'Получить гостя:\n { = }\n')
'''
