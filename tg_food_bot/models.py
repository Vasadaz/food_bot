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
    categories = models.ForeignKey(
        Category,
        verbose_name='Любимая категория блюд',
        db_index=True,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dishes',
    )
    ingredients = models.TextField(
        verbose_name='Ингредиенты',
        default=None,
        blank=True,
        null=True,
    )
    recipe = models.TextField(
        verbose_name='Рецепт приготовления',
        default=None,
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        verbose_name='Показывать блюдо',
        db_index=True,
        default=True,
        null=True,
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Guest(models.Model):
    telegram_id = models.IntegerField(
        verbose_name='Телеграм ID',
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
        blank=True,
        db_index=True,
        null=True,
        region='RU',
    )
    priority_categories = models.ForeignKey(
        Category,
        verbose_name='Любимые категория блюд',
        db_index=True,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='guests',
    )
    likes = models.ManyToManyField(
        Dish,
        verbose_name='Любимые рецепты',
        related_name='like_guests',
        blank=True,
        null=True,
        db_index=True,
    )
    dislikes = models.ManyToManyField(
        Dish,
        verbose_name='Не любимые рецепты',
        related_name='dislike_guests',
        blank=True,
        null=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'гостя'
        verbose_name_plural = 'Гости'

    def __str__(self):
        return self.name
