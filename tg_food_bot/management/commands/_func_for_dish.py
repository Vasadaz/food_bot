import random
from tg_food_bot.models import Category, Dish, Guest

def get_dish_content(dish):
    title = dish.title
    ingredients = dish.ingredients
    recipe = dish.recipe
    message = f'{title} \n\n {ingredients} \n\n {recipe}'
    collected_dish = {
        'image': dish.image,
        'message': message
    }
    return collected_dish


def get_random_dish():
    dishes = Dish.objects.filter(active=True)
    dish = random.choice(dishes)
    return dish

