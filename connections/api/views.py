from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from .serializers import (
    FollowersSerializer,
    FollowingSerializer,
    get_follow_create_serializer,
    FollowerAcceptSerializer,
)
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsOwnerOrReadOnly,
    IsFollowerOrReadOnly,
    IsFollowingOrReadOnly,
)
from rest_framework.exceptions import ValidationError
from profiles.models import UserProfile
from connections.models import Connection

User = get_user_model()


class FollowersListAPIView(ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        profile = self.request.GET.get("profile")
        if profile:
            qs = Connection.objects.filter(follower__username=self.request.user, following__username=profile,
                                           requested=False)
            if qs.exists():
                return Connection.objects.filter(following__username=profile, requested=False)
            us = UserProfile.objects.get(username=profile)
            if us.is_private:
                raise ValidationError("You are Not Authorized")
            return Connection.objects.filter(following__username=profile, requested=False)
        return Connection.objects.filter(following__username=self.request.user, requested=False)

    class Meta:
        model = Connection


class FollowingListAPIView(ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        profile = self.request.GET.get("profile")
        if profile:
            qs = Connection.objects.filter(follower__username=self.request.user, following__username=profile,
                                           requested=False)
            if qs.exists():
                return Connection.objects.filter(follower__username=profile, requested=False)
            us = UserProfile.objects.get(username=profile)
            if us.is_private:
                raise ValidationError("You are Not Authorized")
            return Connection.objects.filter(follower__username=profile, requested=False)
        return Connection.objects.filter(follower__username=self.request.user, requested=False)

    class Meta:
        model = Connection

# related following and requests


class FollowRequestListAPIView(ListAPIView):
    queryset = Connection.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated, IsFollowingOrReadOnly]

    def get_queryset(self):
        return Connection.objects.filter(following=self.request.user, requested=True)

    class Meta:
        model = Connection


class FollowRequestAcceptAPIView(UpdateAPIView):
    lookup_field = 'slug'
    queryset = Connection.objects.all()
    serializer_class = FollowerAcceptSerializer
    permission_classes = [IsAuthenticated, IsFollowingOrReadOnly]

    def get_queryset(self):
        return Connection.objects.filter(following=self.request.user, requested=True)

    class Meta:
        model = Connection


class FollowRequestDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    queryset = Connection.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated, IsFollowingOrReadOnly]

    def get_queryset(self):
        return Connection.objects.filter(following=self.request.user, requested=True)

    class Meta:
        model = Connection


class ConnectionCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated, IsFollowerOrReadOnly]

    def get_queryset(self):
        username = self.request.GET.get("user")
        return UserProfile.objects.filter(username=username)

    def get_serializer_class(self):
        username = self.request.GET.get("user")
        return get_follow_create_serializer(following=username, follower=self.request.user)

    class Meta:
        model = Connection


class ConnectionDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    queryset = Connection.objects.all()
    serializer_class = FollowingListAPIView
    permission_classes = [IsAuthenticated, IsFollowerOrReadOnly]

    class Meta:
        model = Connection
