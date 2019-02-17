from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)
