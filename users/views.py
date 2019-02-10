from django.views.generic import DetailView

from .models import CustomUser


class UserInfoDetailView(DetailView):
    model = CustomUser
    template_name = 'users/user_info.html'
    context_object_name = 'user_info'
