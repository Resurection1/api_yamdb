from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError('Данный логин нельзя выбрать.')
