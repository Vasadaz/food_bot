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

    if guest_categories.count() == 0:
        dishes = Dish.objects.filter(
            active=True,
            price__lte=guest_budget
        ).exclude(
            title__in=guest_dislikes | guest_likes,
        )
    else:
        dishes = Dish.objects.all()
        for category in guest_categories:
            category_dishes = Dish.objects.filter(
                active=True,
                categories=category,
                price__lte=guest_budget
            ).exclude(
                title__in=guest_dislikes | guest_likes,
            )
            dishes = dishes & category_dishes

    dish = random.choice(dishes)
    return dish

def get_dish(title):
    return Dish.objects.get(title=title)