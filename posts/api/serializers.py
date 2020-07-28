from rest_framework import serializers
from posts.models import PostFeed
from rest_framework.serializers import HyperlinkedIdentityField


class PostListSerializer(serializers.ModelSerializer):
    detail_url = HyperlinkedIdentityField(lookup_field='slug', view_name='post_detail_api')
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostFeed
        fields = [
            'detail_url',
            'user',
            'slug',
            'published_date',
            'caption',
        ]
        read_only_fields = ['user', 'slug', 'published_date', 'caption']
        ordering = ['published_date']

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostFeed
        fields = [
            'user',
            'slug',
            'published_date',
            'caption',
        ]
        read_only_fields = ['user', 'slug']

    def get_user(self, obj):
        return str(obj.user.username)



