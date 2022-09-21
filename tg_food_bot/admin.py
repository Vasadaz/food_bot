from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Dish, Guest, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    list_per_page = 15


class GuestAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'name',
        'phonenumber',
        'priority_categories',
    )
    raw_id_fields = (
        'likes',
        'dislikes',
    )
    list_per_page = 15


class DishAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'image',
        'preview',
        'categories',
        'ingredients',
        'recipe',
        'active',
    ]
    list_display = (
        'title',
        'categories',
        'active',
    )
    list_filter = ('categories',)
    list_editable = ('active',)
    list_per_page = 15
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Dish, DishAdmin)
