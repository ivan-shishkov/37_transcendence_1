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
        'user avatar', upload_to='avatars/', blank=True, default='')
    description = models.TextField('about me', blank=True, default='')

    friends = models.ManyToManyField('self', symmetrical=False)

    class Meta:
        ordering = ('last_name', 'first_name',)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('users:user_detail', args=[str(self.id)])
