import random

from tg_food_bot.models import Category, Dish, Guest


def get_dish_content(dish):
    title = dish.title
    ingredients = dish.ingredients
    recipe = dish.recipe
    price = dish.price
    message = f'{title}\n\n' \
              f'{ingredients}\n\n' \
              f'{recipe}\n\n' \
              f'Стоимость одной порции {price}.'

    collected_dish = {
        'image': dish.image,
        'message': message
    }
    return collected_dish


def get_random_dish(guest: Guest):
    guest_budget = guest.budget
    guest_categories = guest.priority_categories.all()
    guest_dislikes = guest.dislikes.all()
    guest_likes = guest.likes.all()

    if not guest_budget:
        dishes = Dish.objects.all().order_by('-price')
        guest_budget = dishes[0].price

    if not guest_categories:
        guest_categories = Category.objects.all()

    dishes = Dish.objects.filter(
        active=True,
        categories__in=guest_categories,
        price__lte=guest_budget
    ).exclude(
        title__in=guest_dislikes | guest_likes,
    )

    dish = random.choice(dishes)
    return dish
