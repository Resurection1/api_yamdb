import datetime

from django.core.exceptions import ValidationError


def max_year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f'{value} неверный год!',
            params={'value': value},
        )
