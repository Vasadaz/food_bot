from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Dish(models.Model):
    VEGAN = 'VG'
    FISH = 'FH'
    SALADS = 'SL'
    GLUTEN = 'GL'

    TYPE_CHOICES = [
        (VEGAN, 'Вегатарианские блюда'),
        (FISH, 'Рыбные блюда'),
        (SALADS, 'Салаты'),
        (GLUTEN, 'Блюда без глютена'),
    ]

    title = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images',
        null=True,
    )
    category = models.CharField(
        verbose_name='Категория',
        db_index=True,
        max_length=2,
        choices=TYPE_CHOICES,
        blank=True,
        primary_key=True,
    )
    ingredients = models.TextField(
        verbose_name='Ингредиенты',
    )
    recipe = models.TextField(
        verbose_name='Рецепт приготовления',
    )
    active = models.BooleanField(
        verbose_name='Показать гостям',
        db_index=True,
        null=True,
        default=True,
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Guest(models.Model):
    telegram_id = models.IntegerField(
        verbose_name='Телеграм ID',
        unique=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    phonenumber = PhoneNumberField(
        verbose_name='Номер телефона',
        db_index=True,
        region='RU',
        blank=True,
        null=True,

    )
    priority_category = models.ForeignKey(
        Dish,
        verbose_name='Любимая категория блюд',
        db_index=True,
        related_name='guests',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    likes = models.ManyToManyField(
        Dish,
        verbose_name='Любимые рецепты',
        related_name='like_guests',
        blank=True,
        db_index=True,
    )
    dislikes = models.ManyToManyField(
        Dish,
        verbose_name='Не любимые рецепты',
        related_name='dislike_guests',
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'гостя'
        verbose_name_plural = 'Гости'

    def __str__(self):
        return self.name
