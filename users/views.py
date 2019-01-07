from django.views.generic import DetailView
from django.contrib.auth.models import User


class UserInfoDetailView(DetailView):
    model = User
    template_name = 'users/user_info.html'
    context_object_name = 'user_info'
