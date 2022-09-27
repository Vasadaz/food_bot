from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Dish, Guest, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    list_per_page = 15


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'telegram_id',
        'phonenumber',
    )
    raw_id_fields = (
        'likes',
        'dislikes',
        'priority_categories',
    )
    list_per_page = 15


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'image',
        'preview',
        'categories',
        'ingredients',
        'recipe',
        'price_portion',
        'active',
    ]
    list_display = (
        'title',
        'active',
    )
    list_filter = ('categories',)
    list_editable = ('active',)
    list_per_page = 15
    raw_id_fields = ('categories',)
    readonly_fields = ['preview']

    @admin.display(description='Превью изображения')
    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
