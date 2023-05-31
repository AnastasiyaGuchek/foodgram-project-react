from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    """Встроенный класс для отображения модели IngredientInRecipe."""
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про рецепты."""
    inlines = (RecipeIngredientInline, )
    list_display = (
        'id',
        'name',
        'author',
        'in_favorites',
        'pub_date',
    )
    list_filter = ('name', 'author', 'tags',)
    search_fields = ['name']

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про теги."""
    list_display = (
        'id',
        'name',
        'slug',
        'color',
    )
    list_filter = ('name', 'color',)
    search_fields = ['name', 'color']
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про ингредиенты."""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ['name']


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про ингредиенты в рецептах."""
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ['recipe', 'ingredient']
    list_filter = ('recipe', 'ingredient')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про избранные рецепты."""
    list_display = ('id', 'user', 'recipe')
    search_fields = ['user', 'recipe']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про список покупок."""
    list_display = ('id', 'user', 'recipe')
    search_fields = ['user', 'recipe']
