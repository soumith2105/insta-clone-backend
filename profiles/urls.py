from django.urls import path

from .views import UpdateProfileView, CreateProfileView, ChangePasswordView, ProfileDetailView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name="profiles/login_form.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', UpdateProfileView.as_view(), name='update'),
    path('password/change/', ChangePasswordView.as_view(), name='changepassword'),
    path('signup/', CreateProfileView.as_view(), name='signup'),
    path('<username>/',  ProfileDetailView.as_view(), name='profile_info'),
]
