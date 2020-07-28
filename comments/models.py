from django.db import models
from profiles.models import UserProfile
from posts.models import PostFeed
import string as str
from random import choice

# Create your models here.


def generate_id():
    n = 10
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits + '_'
    return ''.join(choice(random) for _ in range(n))


class CommentManager(models.Manager):
    def create_comment(self, sender, slug, comment_text):
        model_qs = PostFeed.objects.filter(slug=slug)
        if model_qs.exists() and model_qs.count() == 1:
            instance = self.model()
            instance.comment_on = model_qs.first()
            instance.sender = sender
            instance.comment_text = comment_text
            instance.save()
            return instance
        return None


class ReplyCommentManager(models.Manager):
    def create_reply(self, sender, slug, reply_text):
        model_qs = Comment.objects.filter(slug=slug)
        if model_qs.exists() and model_qs.count() == 1:
            instance = self.model()
            instance.reply_on = model_qs.first()
            instance.reply_sender = sender
            instance.reply_text = reply_text
            instance.save()
            return instance
        return None


class Comment(models.Model):
    comment_on = models.ForeignKey(PostFeed, on_delete=models.CASCADE, related_name='comment_on')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_sender')
    slug = models.SlugField(unique=True, max_length=35, default=generate_id)
    comment_text = models.TextField(null=False, blank=False)
    commented_time = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-commented_time']


class ReplyComment(models.Model):
    reply_on = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_on_comment')
    slug = models.SlugField(unique=True, max_length=12, default=generate_id)
    reply_sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_reply_by')
    reply_text = models.TextField(null=False, blank=False)
    reply_time = models.DateTimeField(auto_now_add=True)

    objects = ReplyCommentManager()

    class Meta:
        ordering = ['-reply_time']
