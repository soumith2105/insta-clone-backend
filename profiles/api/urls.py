from django.urls import path
from .views import (
    CreateUserAPIView,
    ModifyUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView,
    ChangePasswordAPIView,
    DetailUserAPIView,
)


urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('pwdchange/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('<username>/', DetailUserAPIView.as_view(), name='profile-info'),
    path('<username>/edit/', ModifyUserAPIView.as_view(), name='update-info'),
]
