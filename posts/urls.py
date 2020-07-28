from django.urls import path
from .views import (
    ListPostView,
    DetailPostView,
    UpdatePostView,
    CreatePostView,
    DeletePostView
)


urlpatterns = [
    path('', ListPostView.as_view(), name='post_list'),
    path('create/', CreatePostView.as_view()),
    path('<str:slug>/', DetailPostView.as_view(), name='post_detail'),
    path('<str:slug>/edit/', UpdatePostView.as_view(), name='post_edit'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='post_delete'),
]
