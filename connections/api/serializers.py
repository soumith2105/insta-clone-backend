from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from profiles.models import UserProfile
from connections.models import Connection

User = get_user_model()


class FollowerAcceptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = [
            'requested',
        ]
        read_only_fields = ['follower', 'request_slug']


class FollowersSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following_slug = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = [
            'follower',
            'following_slug',
        ]

    def get_follower(self, obj):
        return str(obj.follower.username)

    def get_following_slug(self, obj):
        return str(obj.slug)


class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    following_slug = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = [
            'following',
            'following_slug',
        ]

    def get_following(self, obj):
        return str(obj.following.username)

    def get_following_slug(self, obj):
        return str(obj.slug)


def get_follow_create_serializer(following=None, follower=None):

    class FollowCreateSerializer(serializers.ModelSerializer):
        follower_name = serializers.SerializerMethodField()
        following_name = serializers.SerializerMethodField()

        class Meta:
            model = Connection
            fields = [
                'follower_name',
                'following_name',
            ]
            read_only_fields = ['follower', 'following', ]

        def __init__(self, *args, **kwargs):
            super(FollowCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            qs = Connection.objects.filter(follower=follower, following__username=following)
            if qs.exists() and qs.count() == 1:
                raise ValidationError('Connection Does Exists')
            else:
                user = UserProfile.objects.filter(username=following)
                if not user.exists() and user.count() == 1:
                    raise ValidationError('User Does Not Exists')
            return data

        def create(self, validated_data):
            username = UserProfile.objects.filter(username=following).first()
            connection = Connection.objects.create_connection(follower=follower, following=username)
            return connection

        def get_follower_name(self, obj):
            return str(obj.follower.username)

        def get_following_name(self, obj):
            return str(obj.following.username)

    return FollowCreateSerializer
