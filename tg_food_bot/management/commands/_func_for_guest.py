import phonenumbers

from tg_food_bot.models import Category, Dish, Guest


def add_categories_to_guest(guest: Guest, categories: list):
    for category in categories:
        if category:
            category_obj = Category.objects.get(
                title=category,
            )
            guest.priority_categories.add(category_obj)


def change_category_to_guest(guest: Guest, category: str):
    category_obj = Category.objects.get(
        title=category,
    )
    if category_obj in guest.priority_categories.all():
        guest.priority_categories.remove(category)
    else:
        guest.priority_categories.add(category_obj)

# def remove_category_from_guest(guest: Guest, category: str):
#     guest.priority_categories.remove(category)

def create_guest(telegram_id: int):
    guest, created = Guest.objects.get_or_create(
        telegram_id=telegram_id,
    )
    return created


def delete_guest(telegram_id: int):
    guest = Guest.objects.get(
        telegram_id=telegram_id,
    )
    guest.delete()


def add_guest_name(guest, name):
    guest.name = name
    guest.save()


def add_guest_phonenumber(guest: Guest, phonenumber: str):
    if not normalize_owners_phonenumber(phonenumber):
        return False
    else:
        guest.phonenumber = normalize_owners_phonenumber(phonenumber)
        guest.save()
        return True


def add_new_categories_to_guest(guest: Guest, categories: list):
    remove_categories_of_guest(guest)
    add_categories_to_guest(guest, categories)


def get_guest(telegram_id: int) -> Guest:
    guest = Guest.objects.get(
        telegram_id=telegram_id,
    )

    return guest


def get_guest_categories(guest: Guest) -> Guest:
    guest_categories = guest.priority_categories.all()

    return guest_categories


def get_guest_dislikes(guest: Guest) -> Guest:
    guest_dislikes = guest.dislikes.all()

    return guest_dislikes


def get_guest_likes(guest: Guest) -> Guest:
    guest_likes = guest.likes.all()

    return guest_likes


def normalize_owners_phonenumber(phonenumber: str):
    normalization_number = phonenumbers.parse(phonenumber, 'RU')
    if not phonenumbers.is_possible_number(normalization_number):
        return False

    international_number = phonenumbers.format_number(
        normalization_number,
        phonenumbers.PhoneNumberFormat.E164
    )

    if not normalization_number.italian_leading_zero:
        return international_number


def remove_categories_of_guest(guest: Guest):
    guest.priority_categories.clear()


def remove_dislike(guest: Guest, dish: Dish):
    guest.dislikes.remove(dish)


def remove_like(guest: Guest, dish: Dish):
    guest.likes.remove(dish)


def set_budget(guest: Guest, budget: int):
    guest.budget = budget
    guest.save()


def set_dislike(guest: Guest, dish: Dish):
    remove_like(guest, dish)
    guest.dislikes.add(dish)


def set_like(guest: Guest, dish: Dish):
    remove_dislike(guest, dish)
    guest.likes.add(dish)
