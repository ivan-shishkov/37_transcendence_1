from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.contrib.auth import password_validation
from captcha.fields import CaptchaField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)

    def _post_clean(self):
        super(UserCreationForm, self)._post_clean()

        password = self.cleaned_data.get('password1')

        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)
