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


def add_dish(dish: dict):
    title = dish['title']

    if not Dish.objects.filter(title=title):
        dish_obj = Dish(
            title=title,
            image=dish['image'],
            ingredients='\n'.join(dish['ingredients']),
            recipe='\n'.join(dish['recipe']),
        )
        dish_obj.save()

        add_categories_to_dish(dish_obj, dish['categories'])

        print('Add dish:', dish_obj)
    else:
        print('DUBLLE:', title)


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
