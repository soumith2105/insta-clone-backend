from django.db import models
from django.db.models import Q
from django.conf import settings
import string as str
from random import choice
# Create your models here.

User = settings.AUTH_USER_MODEL


def generate_id():
    n = 8
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits + '_'
    return ''.join(choice(random) for _ in range(n))


class PostFeedQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
                    Q(user__username__icontains=query) |
                    Q(caption__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__full_name__icontains=query) |
                    Q(user__email_id__icontains=query)
                    )

        return self.filter(lookup)


class PostFeedManager(models.Manager):
    def get_queryset(self):
        return PostFeedQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class PostFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=25, default=generate_id)
    published_date = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(null=True, blank=True)

    objects = PostFeedManager()

    def __str__(self):
        return f"{self.user.username}:{self.caption}"

    class Meta:
        ordering = ['-published_date']

    def get_absolute_url(self):
        return f"/posts/{ self.slug }"

    def get_edit_url(self):
        return f"{ self.get_absolute_url() }/edit"

    def get_delete_url(self):
        return f"{ self.get_absolute_url() }/delete"
