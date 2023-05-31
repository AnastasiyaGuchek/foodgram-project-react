from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    '''Модель ингридиентов.'''
    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=settings.RECIPES_MAX_LENGHT,
        blank=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.UNIT_MAX_LENGHT,
        blank=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    '''Модель тегов.'''
    name = models.CharField(
        verbose_name='Тег',
        unique=True,
        max_length=settings.TAG_MAX_LENGHT
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=settings.COLOR_MAX_LENGHT,
        validators=[
            RegexValidator(
                regex='^#([a-fA-F0-9]{6})',
                message='Введите значение цвета в формате HEX! Пример:#FF0000'
            )
        ]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Модель рецептов.'''
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=settings.RECIPES_MAX_LENGHT
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        max_length=settings.RECIPES_MAX_LENGHT,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1, 'Время приготовления должно быть не менее минуты'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    '''Модель для связи рецепта и ингредиентов.'''
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1, 'В рецепте должен быть как минимум один ингредиент.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        ordering = ('recipe', )

    def __str__(self):
        return (f'В рецепте {self.recipe.name} {self.amount} '
                f'{self.ingredient.measurement_unit} {self.ingredient.name}')


class Favorite(models.Model):
    '''Модель для избранных рецептов.'''
    user = models.ForeignKey(
        User,
        related_name='Favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='FavoriteRecipe',
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в список избранных'


class ShoppingCart(models.Model):
    '''Рецепты, добавленные в список покупок.'''
    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в список покупок'
