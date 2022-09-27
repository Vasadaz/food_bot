from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        primary_key=True,
        unique=True,
    )

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.title


class Dish(models.Model):
    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
        primary_key=True,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True,
        null=True,
        upload_to='images',
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        blank=True,
        db_index=True,
        related_name='dishes',
    )
    ingredients = models.TextField(
        verbose_name='Ингредиенты',
        blank=True,
        null=True,
    )
    recipe = models.TextField(
        verbose_name='Рецепт',
        blank=True,
        null=True,
    )
    price = models.SmallIntegerField(
        verbose_name='Цена порции',
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        verbose_name='Показывать блюдо',
        db_index=True,
        default=True,
    )

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.title


class Guest(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        blank=True,
        null=True,
        max_length=200,
    )
    telegram_id = models.IntegerField(
        verbose_name='Телеграм ID',
        unique=True,
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
        blank=True,
        db_index=True,
        null=True,
        region='RU',
    )
    priority_categories = models.ManyToManyField(
        Category,
        verbose_name='Любимые категория блюд',
        db_index=True,
        blank=True,
        related_name='guests',
    )
    budget = models.IntegerField(
        verbose_name='Бюджет',
        blank=True,
        null=True,
    )
    likes = models.ManyToManyField(
        Dish,
        verbose_name='Любимые рецепты',
        blank=True,
        db_index=True,
        related_name='like_guests',
    )
    dislikes = models.ManyToManyField(
        Dish,
        verbose_name='Не любимые рецепты',
        blank=True,
        db_index=True,
        related_name='dislike_guests',
    )

    class Meta:
        verbose_name = 'гостя'
        verbose_name_plural = 'Гости'

    def __str__(self):
        return self.name
