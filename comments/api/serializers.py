from rest_framework import serializers
from comments.models import Comment, ReplyComment
from posts.models import PostFeed
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    post_owner = serializers.SerializerMethodField()
    comment_on_post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'comment_on',
            'sender',
            'slug',
            'comment_on_post',
            'post_owner',
            'comment_text',
            'commented_time',
        ]
    read_only_fields = ['commented_time', 'sender', 'comment_on']

    def get_post_owner(self, obj):
        return str(obj.comment_on.user.username)

    def get_comment_on_post(self, obj):
        return str(obj.comment_on.caption)


class CommentDetailSerializer(serializers.ModelSerializer):
    post_owner = serializers.SerializerMethodField()
    comment_on_post = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'comment_on',
            'sender',
            'slug',
            'comment_on_post',
            'post_owner',
            'comment_text',
            'commented_time',
            'replies',
        ]
    read_only_fields = ['commented_time', 'sender', 'comment_on']

    def get_replies(self, obj):
        return ReplyCommentSerializer(ReplyComment.objects.filter(reply_on=obj), many=True).data

    def get_post_owner(self, obj):
        return str(obj.comment_on.user.username)

    def get_comment_on_post(self, obj):
        return str(obj.comment_on.caption)


def get_comment_create_serializer(slug=None, sender=None):

    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'comment_on',
                'sender',
                'comment_text',
                'commented_time',
            ]
            read_only_fields = ['commented_time', 'sender', 'comment_on']

        def __init__(self, *args, **kwargs):
            qs = PostFeed.objects.filter(slug=slug)
            if qs.exists() and qs.count() == 1:
                self.comment_on = qs.first()
                self.sender = sender
            super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            qs = PostFeed.objects.filter(slug=slug)
            if not qs.exists() and qs.count() == 1:
                raise ValidationError('Post does not exist')
            return data

        def create(self, validated_data):
            comment_text = validated_data.get("comment_text")
            comment = Comment.objects.create_comment(sender, slug, comment_text)
            return comment

    return CommentCreateSerializer


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyComment
        fields = [
            'reply_on',
            'slug',
            'reply_sender',
            'reply_text',
            'reply_time',
        ]
        read_only_fields = ['slug', 'reply_sender', 'reply_time', 'reply_on']


def get_reply_create_serializer(slug=None, sender=None):

    class ReplyCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = ReplyComment
            fields = [
                'reply_on',
                'slug',
                'reply_sender',
                'reply_text',
                'reply_time',
            ]
            read_only_fields = ['slug', 'reply_sender', 'reply_time', 'reply_on']

        def __init__(self, *args, **kwargs):
            qs = Comment.objects.filter(slug=slug)
            if qs.exists() and qs.count() == 1:
                self.reply_on = qs.first()
                self.reply_sender = sender
            super(ReplyCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            qs = Comment.objects.filter(slug=slug)
            if not qs.exists() and qs.count() == 1:
                raise ValidationError('Comment does not exist')
            return data

        def create(self, validated_data):
            reply_text = validated_data.get("reply_text")
            reply = ReplyComment.objects.create_reply(sender, slug, reply_text)
            return reply

    return ReplyCreateSerializer
