from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.query import QuerySet
from django.conf import settings
import uuid, os, datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askserver.settings')

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, uid, password=None, **extra_fields):
        if not uid:
            raise ValueError('The given UID must be set')
        permissions = extra_fields.pop('permissions', 1)
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
        permissions = extra_fields.pop('permissions', 7)
        user = self.model(uid=uid, permissions=permissions, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    displayname = models.CharField(max_length=255, blank=True, null=True)
    pronouns = models.CharField(max_length=50, blank=True, null=True)
    permissions = models.IntegerField(default=1)  
    tags = models.ManyToManyField(Tag, related_name='userTagSubscriptions')
    objects = UserManager()
    password = models.CharField(max_length=128, default=make_password(None))
    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    # Stealing from those better than me.
    # https://github.com/django/django/blob/c187f5f9242b681abaa199173e02066997439425/django/contrib/auth/models.py#L360C5-L364C6
    is_staff = models.BooleanField(
        default=False,
    )

    def dead():
        """A magic value so the loss of a record (GDPR) doesn't cascade
        (unless it needs to, of course)
        """
        return User.objects.get_or_create(uid="DEADBEEF", permissions=0)

    def __str__(self):
        """Users as strings will be represented by their UID.
        """
        return self.uid


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey('Thread', related_name='messages', on_delete=models.CASCADE, null=False, blank=False, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')
    date = models.DateTimeField(db_index=True)
    voters = models.ManyToManyField(User, related_name='user_votes')
    reply = models.ForeignKey('self', related_name='replies', on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField()
    hidden = models.BooleanField(default=False)
    question = models.BooleanField(default=False, null=False)

    @property
    def votes(self):
        return self.voters.all().count()

    def __str__(self):
        """Messages as strings will be represented by their UUID.
        """
        return str(self.id)

    def dead():
        # weird special case for deleted messages which shouldn't cascade.
        return Message.objects.get_or_create(id=uuid.UUID(int = 0), author=User.dead())

    def as_api(self):
        return {
            "_METADATA": "message.askhole.api.dotfile.sh/v1alpha1",
            "id": str(self),
            "threadID": str(self.thread),
            # The first time, skip anonymous logic. It will never be anonymous anyway
            # as the author can always de-anonymize themself.
            "author": {
                "uid": str(self.author),
                "displayname": self.author.displayname,
                "pronouns": self.author.pronouns
            },
            "date": int(self.date.timestamp()),
            "votes": self.votes,
            "reply": str(self.reply) if self.reply is not None else None,
            "body": self.body,
            "hidden": self.hidden,
            "question": self.question
        }

    # This assures only a single Message in the set of all messages which have
    # the same `thread` value can have the `question` field set to True.
    # This question is set, in application logic, at the creation of the thread.
    class Meta:
        constraints = [
            UniqueConstraint(name='question_message', fields=['thread', 'question'], condition=models.Q(question=True))
        ]

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    anonymous = models.BooleanField(default=False, null=False)
    communityaward = models.ForeignKey(Message, related_name='community_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    authoraward = models.ForeignKey(Message, related_name='author_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    instructoraward = models.ForeignKey(Message, related_name='instructor_award_threads', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='threads')

    # Any value needed for both Threads and Messages are stored in messages to
    # keep data consistent. Properties are established if threads need them too
    @property
    def author(self) -> User:
        return self.question_message.author
    @property
    def date(self) -> datetime.datetime:
        return self.question_message.date
    @property
    def hidden(self) -> bool:
        return self.question_message.hidden
    @property
    def question_message(self) -> Message:
        return self.messages.get(question=True)
    @property
    def responses(self) -> QuerySet['Message']:
        """This gets all responses (messages that are not questions)
        They are ordered chronologically
        """
        return self.messages.filter(question=False).order_by('date')
    
    def __str__(self):
        """Threads as strings will be represented by their UUID.
        """
        return str(self.id)

    def as_api(self):
        """Get all responses to the thread as a BASE api object.
        Warning: This does not anonymize."""
        return {
            "_METADATA": "thread.askhole.api.dotfile.sh/v1alpha1",
            "id": str(self),
            "title": self.title,
            "anonymous": self.anonymous,
            "question": self.question_message.as_api(),
            "responses": [r.as_api() for r in self.responses],
            "communityAward": str(self.communityaward),
            "authorAward": str(self.authoraward),
            "instructorAward": str(self.instructoraward),
            "tags": list(self.tags.values_list('name', flat=True))
        }



class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    comment = models.TextField(null=True, blank=True)

