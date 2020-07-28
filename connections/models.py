from django.db import models
from django.db.models import Q
import string as str
from random import choice
from profiles.models import UserProfile


def generate_id():
    n = 8
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits + '_'
    return ''.join(choice(random) for _ in range(n))


# Create your models here.


class ConnectionQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
            Q(following__username__icontains=query) |
            Q(following__full_name__icontains=query) |
            Q(following__email_id__icontains=query) |
            Q(following__mobile_number__icontains=query)
        )

        return self.filter(lookup)


class ConnectionManager(models.Manager):

    def get_queryset(self):
        return ConnectionQuerySet(self.model, using=self._db)

    def create_connection(self, follower, following):
        instance = self.model()
        instance.follower = follower
        instance.following = following
        if instance.following.is_private:
            instance.requested = True
        else:
            instance.requested = False
        instance.save()
        return instance


class Connection(models.Model):
    slug = models.SlugField(default=generate_id, null=False, blank=False)
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    requested = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.follower.username}>{self.following.username}"

    objects = ConnectionManager()
