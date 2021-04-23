from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class CreationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email", "password1")

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)
