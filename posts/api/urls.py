from django.urls import path
from .views import (
    ListPostAPIView,
    DetailPostAPIView,
    UpdatePostAPIView,
    CreatePostAPIView,
    DeletePostAPIView,
)


urlpatterns = [
    path('', ListPostAPIView.as_view(), name='post_list_api'),
    path('create/', CreatePostAPIView.as_view(), name='post_create_api'),
    path('<str:slug>/', DetailPostAPIView.as_view(), name='post_detail_api'),
    path('<str:slug>/edit/', UpdatePostAPIView.as_view(), name='post_update_api'),
    path('<str:slug>/delete/', DeletePostAPIView.as_view(), name='post_delete_api'),
]
