from rest_framework import serializers
from likes.models import PostLike, CommentLike, ReplyCommentLike
from posts.models import PostFeed
from comments.models import Comment, ReplyComment
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class PostLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostLike
        fields = [
            'user',
            'post',
            'liked_time',
        ]
        read_only_fields = ['user', 'post', 'liked_time', ]


class CommentLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = [
            'user',
            'comment',
            'liked_time',
        ]
        read_only_fields = ['user', 'comment', 'liked_time', ]


class ReplyLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyCommentLike
        fields = [
            'user',
            'reply',
            'liked_time',
        ]
        read_only_fields = ['user', 'reply', 'liked_time', ]


def get_create_post_like_serializer(sender=None, slug=None):

    class PostLikeCreateSerializer(serializers.ModelSerializer):

        class Meta:
            model = PostLike
            fields = [
                'user',
                'post',
                'liked_time',
            ]

        def validate(self, data):
            qs = PostFeed.objects.filter(slug=slug)
            if not qs.exists():
                raise ValidationError("Post Does Not Exists")
            return data

        def create(self, validated_data):
            post = PostFeed.objects.get(slug=slug)
            like = PostLike.objects.filter(user=sender, post=post)
            if not like.exists():
                reply = PostLike.objects.create_like(user=sender, post=post)
                return reply
            reply = PostLike.objects.delete_like(user=sender, post=post)
            return reply

    return PostLikeCreateSerializer


def get_create_comment_like_serializer(sender=None, slug=None):

    class CommentLikeCreateSerializer(serializers.ModelSerializer):

        class Meta:
            model = CommentLike
            fields = [
                'user',
                'comment',
                'liked_time',
            ]

        def validate(self, data):
            qs = Comment.objects.filter(slug=slug)
            if not qs.exists():
                raise ValidationError("Comment Does Not Exists")
            return data

        def create(self, validated_data):
            comment = Comment.objects.get(slug=slug)
            like = CommentLike.objects.filter(user=sender, comment=comment)
            if not like.exists():
                reply = CommentLike.objects.create_like(user=sender, comment=comment)
                return reply
            reply = CommentLike.objects.delete_like(user=sender, comment=comment)
            return reply

    return CommentLikeCreateSerializer


def get_create_reply_comment_like_serializer(sender=None, slug=None):

    class ReplyCommentLikeCreateSerializer(serializers.ModelSerializer):

        class Meta:
            model = ReplyCommentLike
            fields = [
                'user',
                'reply',
                'liked_time',
            ]

        def validate(self, data):
            qs = ReplyComment.objects.filter(slug=slug)
            if not qs.exists():
                raise ValidationError("Reply to Comment Does Not Exists")
            return data

        def create(self, validated_data):
            reply = ReplyComment.objects.get(slug=slug)
            like = ReplyCommentLike.objects.filter(user=sender, reply=reply)
            if not like.exists():
                obj = ReplyCommentLike.objects.create_like(user=sender, reply=reply)
                return obj
            obj = ReplyCommentLike.objects.delete_like(user=sender, reply=reply)
            return obj

    return ReplyCommentLikeCreateSerializer


class PostLikesByYouSerializer(serializers.ModelSerializer):
    postuser = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = [
            'postuser',
        ]

    def get_postuser(self, obj):
        return str(obj.post.user.username)
