import json

from pathlib import Path

from django.core.management.base import BaseCommand

from tg_food_bot.models import Dish, Category


DISHES_PATH = Path('static/recipes.json')


def add_categories_to_dish(dish_obj, categories: list):
    for category in categories:
        if category:
            category_obj, created = Category.objects.get_or_create(
                title=category,
            )
            dish_obj.categories.add(category_obj)


def add_dish(dish_notes: dict):
    categories = dish_notes['categories']
    title = dish_notes['title']

    dish_obj, created  = Dish.objects.get_or_create(
                title=title,
            )

    if created:
        dish_obj = Dish(
            title=title,
            image=dish_notes['image'],
            ingredients='\n'.join(dish_notes['ingredients']),
            recipe='\n'.join(dish_notes['recipe']),
            price=dish_notes['price']
        )
        dish_obj.save()

        add_categories_to_dish(dish_obj, categories)

        print('Add dish:', dish_obj)
    else:
        add_categories_to_dish(dish_obj, categories)
        print(f'\033[93mDOUBLE:\033[92m set categories \033[0m{dish_obj.categories.all()}\033[92m for \033[0m{dish_obj}\033[0m')


def main():
    with open(DISHES_PATH, 'r', encoding='utf-8') as file:
        dishes = json.load(file)

    for category, dishes in dishes.items():
        for dish in dishes:
            add_dish(dish)


class Command(BaseCommand):
    help = 'Start adding dishes'

    def handle(self, *args, **options):
        main()
