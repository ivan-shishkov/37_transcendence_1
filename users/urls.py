from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserInfoDetailView, SignUpView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserInfoDetailView.as_view(), name='user_info'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
