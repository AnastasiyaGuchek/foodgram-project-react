from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=settings.USERS_MAX_LENGTH,
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.EMAIL_MAX_LENGTH,
        blank=False,
        null=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.USERS_MAX_LENGTH,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.USERS_MAX_LENGTH,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.USERS_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'email')
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username'
            )
        ]

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки на авторов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
