from django.db import models
from django.conf import settings
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askserver.settings')

class UserManager(BaseUserManager):
    def create_user(self, uid, password=None, **extra_fields):
        if not uid:
            raise ValueError('The given UID must be set')
        permissions = extra_fields.pop('permissions', 0)
        user = self.model(uid=uid, permissions=permissions, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    # TODO: DELETE THIS. DIRTY UGLY NO-GOOD VERY BAD BODGE.
    # does the same thing as create_user, which IS used in prod. but
    # sets superuser. this is for testing only and mother of hell
    # should not be used in prod.
    def create_superuser(self, uid, password=None, **extra_fields):
        if not uid:
            raise ValueError('The given UID must be set')
        permissions = extra_fields.pop('permissions', 0)
        user = self.model(uid=uid, permissions=permissions, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    displayname = models.CharField(max_length=255, blank=True, null=True, default="")
    pronouns = models.CharField(max_length=50, blank=True, null=True, default="")
    permissions = models.IntegerField(default=1)  
    objects = UserManager()
    password = models.CharField(max_length=128, default=make_password(None))
    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    # Stealing from those better than me.
    # https://github.com/django/django/blob/c187f5f9242b681abaa199173e02066997439425/django/contrib/auth/models.py#L360C5-L364C6
    is_staff = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.uid


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey('Thread', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    date = models.DateTimeField()
    votes = models.IntegerField(null=True, blank=True, default=0)
    body = models.TextField()
    hidden = models.BooleanField(default=False)
    question = models.BooleanField(default=False)


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads', on_delete=models.CASCADE)
    date = models.DateTimeField()
    communityaward = models.ForeignKey(Message, related_name='community_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    authoraward = models.ForeignKey(Message, related_name='author_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    instructoraward = models.ForeignKey(Message, related_name='instructor_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='threads')


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    comment = models.TextField(null=True, blank=True)

