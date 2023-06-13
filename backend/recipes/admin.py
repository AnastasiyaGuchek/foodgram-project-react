from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = '-пусто-'
    list_filter = ('author', 'name', 'tags')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - данные про рецепты."""
    list_display = (
        'id',
        'name',
        'author',
        'added_in_favorites',
        'pub_date',
    )
    list_filter = ('name', 'author', 'tags',)
    search_fields = ['name']

    @admin.display(description='В избранном')
    def added_in_favorites(self, obj):
        return obj.favorites.all().count()


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
    list_display = ('ingredient', 'amount')
    search_fields = ['ingredient']
    list_filter = ('ingredient',)


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
