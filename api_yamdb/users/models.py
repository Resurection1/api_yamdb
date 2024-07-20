from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    ROLES = (
        ('user', 'user_client'),
        ('moderator', 'moderator_client'),
        ('is_admin', 'admin_client'),
    )

    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='user')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username
