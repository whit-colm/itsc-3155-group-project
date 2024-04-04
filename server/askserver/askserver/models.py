from django.db import models
import uuid
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askserver.settings')


class User(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    displayname = models.CharField(max_length=255, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    permissions = models.IntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey('Thread', related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    date = models.DateTimeField()
    votes = models.IntegerField(null=True, blank=True, default=0)
    body = models.TextField()
    hidden = models.BooleanField(default=False)


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE)
    date = models.DateTimeField()
    communityaward = models.ForeignKey(Message, related_name='community_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    authoraward = models.ForeignKey(Message, related_name='author_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    instructoraward = models.ForeignKey(Message, related_name='instructor_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='threads')


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    comment = models.TextField(null=True, blank=True)
