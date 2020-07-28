from django.urls import path
from .views import (
    LikesListAPIView,
    CommentLikesAPIView,
    ReplyLikesAPIView,
    CreateLikePostAPIView,
    CreateLikeCommentAPIView,
    CreateLikeReplyCommentAPIView,
    PostLikedByYouListAPIView,
)


urlpatterns = [
    path('likedbyme/', PostLikedByYouListAPIView.as_view(), name='posts_liked_by_you'),
    path("post/", LikesListAPIView.as_view(), name='post_likes'),
    path("comment/", CommentLikesAPIView.as_view(), name='comment_likes'),
    path("reply/", ReplyLikesAPIView.as_view(), name='reply_likes'),
    path("postlike/", CreateLikePostAPIView.as_view(), name='post_create_like'),
    path("commentlike/", CreateLikeCommentAPIView.as_view(), name='comment_create_like'),
    path("commentreplylike/", CreateLikeReplyCommentAPIView.as_view(), name='reply_comment_create_like'),
    path("reply/", ReplyLikesAPIView.as_view(), name='reply_likes'),
]
