import phonenumbers

from tg_food_bot.models import Category, Dish, Guest


def add_categories_to_guest(guest: Guest, categories: list):
    for category in categories:
        if category:
            category_obj = Category.objects.get(
                title=category,
            )
            guest.priority_categories.add(category_obj)


def add_guest(guest_notes: dict) -> Guest:
    guest_obj = Guest(
        name=guest_notes['name'],
        telegram_id=guest_notes['telegram_id'],
        phonenumber=normalize_owners_phonenumber(
            guest_notes['phonenumber'],
        )
    )
    guest_obj.save()

    return guest_obj


def add_guest_phonenumber(guest: Guest, phonenumber: str):
    if normalize_owners_phonenumber(phonenumber):
        guest.phonenumber = phonenumber
        guest.save()


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
    international_number = phonenumbers.format_number(
        normalization_number,
        phonenumbers.PhoneNumberFormat.E164
    )

    if not normalization_number.italian_leading_zero:
        return international_number
    else:
        return None


def remove_categories_of_guest(guest: Guest):
    guest.priority_categories.clear()


def remove_dislike(guest: Guest, dish: Dish):
    guest.dislikes.remove(dish)


def remove_like(guest: Guest, dish: Dish):
    guest.likes.remove(dish)


def set_dislike(guest: Guest, dish: Dish):
    remove_like(guest, dish)
    guest.dislikes.add(dish)


def set_like(guest: Guest, dish: Dish):
    remove_dislike(guest, dish)
    guest.likes.add(dish)
