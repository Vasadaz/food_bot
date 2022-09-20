from django.contrib import admin

from .models import Dish, Guest


class DishAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'active',
    )
    list_filter = ('category',)
    list_editable = ('active',)
    list_per_page = 15


class GuestAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'name',
        'phonenumber',
        'priority_category',
    )
    raw_id_fields = (
        'likes',
        'dislikes',
    )
    list_per_page = 15


admin.site.register(Dish, DishAdmin)
admin.site.register(Guest, GuestAdmin)
