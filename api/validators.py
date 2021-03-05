import datetime as dt

from django.core.exceptions import ValidationError


def year_validator(value):
    NOW_YEAR = dt.datetime.now().year
    if NOW_YEAR < value < 1000:
        raise ValidationError(
            'You cannot add a piece from future or before 1000 year AD'
        )
