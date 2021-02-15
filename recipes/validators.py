from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class GreaterThanValidator(BaseValidator):
    message = _('Ensure this value is greater than %(limit_value)s.')

    def compare(self, a, b):
        return a <= b
