from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    get_comment_create_serializer,
    ReplyCommentSerializer,
    get_reply_create_serializer,
)
from comments.models import Comment, ReplyComment
from rest_framework.permissions import IsAuthenticated
from posts.models import PostFeed
from .permissions import IsOwnerOfCommentOrOwnerOfPostOrReadOnly, IsOwnerOfCommentOrOwnerOfReplyOrReadOnly


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_slug = self.request.GET.get("post")
        comment_on = PostFeed.objects.filter(slug=post_slug).first()
        qs = Comment.objects.filter(comment_on=comment_on)
        return qs

    class Meta:
        model = Comment


class CommentDetailAPIView(RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated]

    class Meta:
        model = Comment


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        slug = self.request.GET.get("post")
        return get_comment_create_serializer(slug=slug, sender=self.request.user)


class CommentDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCommentOrOwnerOfPostOrReadOnly]

    class Meta:
        model = Comment


class ReplyDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    queryset = ReplyComment.objects.all()
    serializer_class = ReplyCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCommentOrOwnerOfReplyOrReadOnly]

    class Meta:
        model = ReplyComment


class ReplyCreateAPIView(CreateAPIView):
    queryset = ReplyComment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        slug = self.request.GET.get("comment")
        return get_reply_create_serializer(slug=slug, sender=self.request.user)
