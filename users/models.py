from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'first name', max_length=30, help_text='Required')
    last_name = models.CharField(
        'last name', max_length=150, help_text='Required')
    email = models.EmailField('email address', help_text='Required')
    avatar = models.ImageField(
        'user avatar', upload_to='avatars/', null=True, blank=True)
    description = models.TextField('about me', null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[str(self.id)])
