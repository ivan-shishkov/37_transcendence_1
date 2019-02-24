from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django_registration.backends.one_step.views import RegistrationView

from .models import CustomUser
from .forms import CustomUserCreationForm


class UserInfoDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_detail.html'
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.get_object()
        user = self.request.user

        context['can_edit_profile'] = current_user == user

        context['can_add_to_friends'] = (
                current_user != user and
                not user.friends.filter(id=current_user.id).exists()
        )
        return context


class UserInfoListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/user_list.html'
    paginate_by = 20


class UserInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'users/user_edit.html'
    fields = ('avatar', 'description',)

    def test_func(self):
        return self.get_object() == self.request.user


class AddToFriendsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        redirect_to = request.POST.get('next')

        friend = CustomUser.objects.get(id=friend_id)
        request.user.friends.add(friend)

        return redirect(redirect_to)


class SignUpView(RegistrationView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('pages:home')
    template_name = 'users/signup.html'
