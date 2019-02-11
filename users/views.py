from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser
from .forms import CustomUserCreationForm


class UserInfoDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_info.html'
    context_object_name = 'user_info'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
