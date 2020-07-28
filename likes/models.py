from django.db import models
from posts.models import PostFeed
from profiles.models import UserProfile
from comments.models import ReplyComment, Comment

# Create your models here.


class PostLikeManager(models.Manager):
    def create_like(self, user, post):
        instance = self.model()
        instance.user = user
        instance.post = post
        instance.save()
        return instance

    def delete_like(self, user, post):
        like = PostLike.objects.get(user=user, post=post)
        like.delete()
        return like


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_liked_by_user')
    post = models.ForeignKey(PostFeed, on_delete=models.CASCADE, related_name='liked_post')
    liked_time = models.DateTimeField(auto_now_add=True)

    objects = PostLikeManager()

    def __str__(self):
        return f"{self.user.username} liked {self.post.user}'s post --- {self.post.slug}"

    class Meta:
        ordering = ['-liked_time']


class CommentLikeManager(models.Manager):
    def create_like(self, user, comment):
        instance = self.model()
        instance.user = user
        instance.comment = comment
        instance.save()
        return instance

    def delete_like(self, user, comment):
        like = CommentLike.objects.get(user=user, comment=comment)
        like.delete()
        return like


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_liked_by_user')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='liked_comment')
    liked_time = models.DateTimeField(auto_now_add=True)

    objects = CommentLikeManager()

    def __str__(self):
        return f"{self.user.username} liked {self.comment.sender}'s comment --- {self.comment.slug}"

    class Meta:
        ordering = ['-liked_time']


class ReplyCommentLikeManager(models.Manager):
    def create_like(self, user, reply):
        instance = self.model()
        instance.user = user
        instance.reply = reply
        instance.save()
        return instance

    def delete_like(self, user, reply):
        like = ReplyCommentLike.objects.get(user=user, reply=reply)
        like.delete()
        return like


class ReplyCommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reply_comment_liked_by_user')
    reply = models.ForeignKey(ReplyComment, on_delete=models.CASCADE, related_name='liked_reply_comment')
    liked_time = models.DateTimeField(auto_now_add=True)

    objects = ReplyCommentLikeManager()

    def __str__(self):
        return f"{self.user.username} liked {self.reply.reply_sender}'s reply --- {self.reply.slug}"

    class Meta:
        ordering = ['-liked_time']
