from django.core.exceptions import ValidationError

from api.v1.constants import NAME_ME


def username_validator(value):
    if value == NAME_ME:
        raise ValidationError('Данный логин нельзя выбрать.')
