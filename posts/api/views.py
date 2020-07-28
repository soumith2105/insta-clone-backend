from rest_framework import generics, mixins
from django.db.models import Q

from posts.models import PostFeed
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
)
from connections.models import Connection
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class ListPostAPIView(generics.ListAPIView):
    queryset = PostFeed.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usernames = Connection.objects.filter(follower__username=self.request.user).values_list('following__username'
                                                                                                , flat=True).distinct()
        posts1 = PostFeed.objects.filter(user__username__in=usernames).order_by('-published_date')
        posts2 = PostFeed.objects.filter(user__username=self.request.user)
        posts = posts1 | posts2
        query = self.request.GET.get("q")
        qs = PostFeed.objects.all()
        if query is not None:
            posts = qs.filter(Q(user__username__icontains=query) |
                           Q(caption__icontains=query) |
                           Q(slug__icontains=query) |
                           Q(user__full_name__icontains=query) |
                           Q(user__email_id__icontains=query)
                           ).distinct()
        return posts

    class Meta:
        model = PostFeed


class DetailPostAPIView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PostFeed.objects.all()

    class Meta:
        model = PostFeed


class CreatePostAPIView(generics.CreateAPIView, mixins.CreateModelMixin):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    class Meta:
        model = PostFeed


class UpdatePostAPIView(generics.UpdateAPIView, mixins.UpdateModelMixin):
    lookup_field = 'slug'
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return PostFeed.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    class Meta:
        model = PostFeed


class DeletePostAPIView(generics.DestroyAPIView):
    lookup_field = 'slug'
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return PostFeed.objects.all()

    class Meta:
        model = PostFeed
