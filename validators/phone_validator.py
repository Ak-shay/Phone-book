from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(phone):
    if len(phone)!=10 or not phone.isdigit():
        raise ValidationError(
            _('Mobile should contain 10 digit positive integer'),
        )