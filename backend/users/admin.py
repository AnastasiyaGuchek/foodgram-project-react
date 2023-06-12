from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Кастомизация админ панели - управление пользователями."""
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'password')
    list_filter = ('username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Кастомизация админ панели - управление подписками."""
    list_display = ('id', 'user', 'author')
