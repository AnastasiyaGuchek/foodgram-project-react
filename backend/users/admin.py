from django.contrib import admin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - управление пользователями."""
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'password', 'role')
    list_filter = ('username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - управление подписками."""
    list_display = ('id', 'user', 'author')
