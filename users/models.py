from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[str(self.id)])
