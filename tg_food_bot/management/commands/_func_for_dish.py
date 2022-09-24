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


def get_random_dish(guest: Guest):
    guest_categories = guest.priority_categories
    guest_dislikes = guest.dislikes
    print('-' * 10)
    print(guest_categories)
    print(guest_dislikes)
    print('-' * 10)
    dishes = Dish.objects.filter(
        active=True,
        categories=guest_categories,
    )

    dish = random.choice(dishes)
    return dish
