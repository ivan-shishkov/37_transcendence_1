from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    UserInfoDetailView, UserInfoUpdateView, SignUpView, AddToFriendsView,
)

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserInfoDetailView.as_view(), name='user_detail'),
    path('<int:pk>/edit/', UserInfoUpdateView.as_view(), name='user_edit'),
    path('add-to-friends/', AddToFriendsView.as_view(), name='add_to_friends'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
