from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .constants import ADMIN_LIST_PAGE
from .models import MyUser


@admin.register(MyUser)
class UserAdmin(UserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = 'значение отсутствует'
    list_editable = ('role',)
    list_filter = ('username',)
    list_per_page = ADMIN_LIST_PAGE
    search_fields = ('username', 'role')
