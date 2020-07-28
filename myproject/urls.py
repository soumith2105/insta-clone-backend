"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    home_page,
    about_page
)

urlpatterns = [
    path('posts/', include('posts.urls')),
    path('', home_page),
    path('about/', about_page),
    path('admin/', admin.site.urls),
    path('profile/', include('profiles.urls')),
    path('api/posts/', include('posts.api.urls')),
    path('api/user/', include('profiles.api.urls')),
    path('api/connections/', include('connections.api.urls')),
    path('api/comment/', include('comments.api.urls')),
    path('api/likes/', include('likes.api.urls')),
]