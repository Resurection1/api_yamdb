from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .constants import (
    MAX_LENGTH,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_ROLE,
    USERNAME_CHECK
)
from .validators import username_validator


class MyUser(AbstractUser):
    """Класс для настройки модели юзера."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    CHOICES = [(USER, 'user'),
               (MODERATOR, 'moderator'),
               (ADMIN, 'admin')
               ]

    username = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=USERNAME_CHECK,
            message='Имя пользователя содержит недопустимый символ'
        ),
            username_validator,
        ]
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        verbose_name='email',
        unique=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=CHOICES,
        default='user')

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
