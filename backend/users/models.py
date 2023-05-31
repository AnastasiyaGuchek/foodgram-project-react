from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    GUEST = 'guest'
    AUTHORIZED = 'authorized'
    ADMIN = 'admin'

    USER_ROLES = [
        (GUEST, 'guest'),
        (AUTHORIZED, 'authorized'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=settings.USERS_MAX_LENGHT,
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.EMAIL_MAX_LENGHT,
        blank=False,
        null=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.USERS_MAX_LENGHT,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.USERS_MAX_LENGHT,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.USERS_MAX_LENGHT
    )
    role = models.CharField(
        default='guest',
        choices=USER_ROLES,
        max_length=settings.ROLE_MAX_LENGHT,
        verbose_name='Роль пользователя',
    )

    @property
    def is_guest(self):
        """Проверка прав неавторизованного пользователя."""
        return self.role == self.GUEST

    @property
    def is_authorized(self):
        """Проверка прав авторизованного пользователя."""
        return self.role == self.AUTHORIZED

    @property
    def is_admin(self):
        """Проверка прав админа."""
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

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
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
