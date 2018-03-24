from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_odd(value):
    if bool(value % 2) == False:
        raise ValidationError(
            _('%(value)s is not odd number'),
            params={'value': value},
        )
