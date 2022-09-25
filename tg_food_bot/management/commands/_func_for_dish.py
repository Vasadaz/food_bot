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
    guest_categories = guest.priority_categories.all()
    guest_dislikes = guest.dislikes.all()
    guest_likes = guest.likes.all()

    if not guest_categories:
        guest_categories = Category.objects.all()

    dishes = Dish.objects.filter(
        active=True,
        categories__in=guest_categories,
    ).exclude(
        title__in=guest_dislikes | guest_likes,
    )

    dish = random.choice(dishes)
    return dish
