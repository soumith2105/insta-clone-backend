from rest_framework.generics import ListAPIView, CreateAPIView
from likes.models import PostLike, CommentLike, ReplyCommentLike
from posts.models import PostFeed
from comments.models import Comment, ReplyComment
from .serializers import (
    PostLikesSerializer,
    CommentLikesSerializer,
    ReplyLikesSerializer,
    get_create_post_like_serializer,
    get_create_comment_like_serializer,
    get_create_reply_comment_like_serializer,
    PostLikesByYouSerializer,
)


class LikesListAPIView(ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikesSerializer

    def get_queryset(self):
        post_slug = self.request.GET.get("post")
        likes_on = PostFeed.objects.filter(slug=post_slug).first()
        qs = PostLike.objects.filter(post=likes_on)
        return qs

    class Meta:
        model = PostLike


class CommentLikesAPIView(ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikesSerializer

    def get_queryset(self):
        comment_slug = self.request.GET.get("comment")
        likes_on = Comment.objects.filter(slug=comment_slug).first()
        qs = CommentLike.objects.filter(comment=likes_on)
        return qs

    class Meta:
        model = CommentLike


class ReplyLikesAPIView(ListAPIView):
    queryset = ReplyCommentLike.objects.all()
    serializer_class = ReplyLikesSerializer

    def get_queryset(self):
        reply_slug = self.request.GET.get("reply")
        likes_on = ReplyComment.objects.filter(slug=reply_slug).first()
        qs = ReplyCommentLike.objects.filter(reply=likes_on)
        return qs

    class Meta:
        model = ReplyCommentLike


class CreateLikePostAPIView(CreateAPIView):
    queryset = PostLike.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        post_slug = self.request.GET.get("post")
        return get_create_post_like_serializer(sender=user, slug=post_slug)

    class Meta:
        model = PostLike


class CreateLikeCommentAPIView(CreateAPIView):
    queryset = CommentLike.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        comment_slug = self.request.GET.get("comment")
        return get_create_comment_like_serializer(sender=user, slug=comment_slug)

    class Meta:
        model = CommentLike


class CreateLikeReplyCommentAPIView(CreateAPIView):
    queryset = ReplyCommentLike.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        reply_slug = self.request.GET.get("reply")
        return get_create_reply_comment_like_serializer(sender=user, slug=reply_slug)

    class Meta:
        model = ReplyCommentLike


class PostLikedByYouListAPIView(ListAPIView):
    serializer_class = PostLikesByYouSerializer

    def get_queryset(self):
        qs = PostLike.objects.filter(user=self.request.user)
        return qs

    class Meta:
        model = PostLike
