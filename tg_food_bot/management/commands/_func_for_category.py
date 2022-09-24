from tg_food_bot.models import Category, Dish, Guest


def get_categories() -> list:
    categories = Category.objects.values_list('title', flat=True)
    return list(categories)
