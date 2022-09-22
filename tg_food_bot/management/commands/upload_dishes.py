import json

from pathlib import Path

from django.core.management.base import BaseCommand

from tg_food_bot.models import Dish


DISHES_PATH = Path('static/recipes.json')


def add_dish(dish: dict):
    dish_obj = Dish(
        title=dish['title'],
        image=dish['image'],
        # categories=dish['categories'],
        ingredients=dish['ingredients'],
        recipe=dish['recipe'],
    )
    dish_obj.save()
    print('Add dish:', dish_obj)


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
