from django.urls import path

from accounts.views import *

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshView.as_view(), name='login-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-user/', ChangeUserInfoView.as_view(), name='change-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
