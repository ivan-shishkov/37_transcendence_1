from django.urls import path

from .views import UserInfoDetailView

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserInfoDetailView.as_view(), name='user_info'),
]
