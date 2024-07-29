from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.v1.constants import LIST_PER_PAGE
from users.models import MyUser


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
    list_per_page = LIST_PER_PAGE
    search_fields = ('username', 'role')
