from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.
class UserProfileQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
                    Q(username__icontains=query) |
                    Q(full_name__icontains=query) |
                    Q(email_id__icontains=query) |
                    Q(mobile_number__icontains=query)
                    )

        return self.filter(lookup)


class UserProfileManager(BaseUserManager):
    def get_queryset(self):
        return UserProfileQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

    def create_user(self, username, email_id, full_name, password):

        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email_id=self.normalize_email(email_id).casefold(),
            username=username.casefold(),
            full_name=full_name,
        )

        user.set_password(password)
        user.is_admin = False
        user.is_active = True
        user.is_private = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_id, full_name, password):
        user = self.create_user(
            username.casefold(),
            email_id.casefold(),
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(unique=True, max_length=255)
    email_id = models.EmailField(unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=200, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email_id', ]

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, profiles):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return f"/profile/{ self.username }"
