import datetime

from django.core.exceptions import ValidationError


def max_year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            '%(value)s is not a correcrt year!',
            params={'value': value},
        )
