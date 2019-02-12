from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser
from .forms import CustomUserCreationForm


class UserInfoDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'current_user'


class UserInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'users/user_edit.html'
    fields = ('first_name', 'last_name',)

    def test_func(self):
        return self.get_object() == self.request.user


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
