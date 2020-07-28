from django.urls import path
from .views import (
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDeleteAPIView,
    ReplyCreateAPIView,
    ReplyDeleteAPIView,
    CommentDetailAPIView,
)

urlpatterns = [
    path("", CommentListAPIView.as_view(), name='comment_list'),
    path("reply/create/", ReplyCreateAPIView.as_view(), name='reply_create'),
    path("create/", CommentCreateAPIView.as_view(), name='comment_create'),
    path("reply/<str:slug>/delete/", ReplyDeleteAPIView.as_view(), name='reply_delete'),
    path("<str:slug>/", CommentDetailAPIView.as_view(), name='comment_list'),
    path("<str:slug>/delete/", CommentDeleteAPIView.as_view(), name='comment_delete'),
]

