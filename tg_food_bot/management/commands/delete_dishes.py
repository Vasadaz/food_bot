import json

from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from tg_food_bot.models import Dish


DISHES_PATH = Path('static/recipes.json')


def delete_dish(dish: dict):
    title = dish['title']
    try:
        dish_obj = Dish.objects.get(title=title)
    except ObjectDoesNotExist:
        print('\033[91mNot found dish:\033[0m', title)
        return
    dish_obj.delete()
    print('Delete dish:', title)


def main():
    with open(DISHES_PATH, 'r', encoding='utf-8') as file:
        dishes = json.load(file)

    for category, dishes in dishes.items():
        for dish in dishes:
            delete_dish(dish)


class Command(BaseCommand):
    help = 'Start delete dishes'

    def handle(self, *args, **options):
        main()
