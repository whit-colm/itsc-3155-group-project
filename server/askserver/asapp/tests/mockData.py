from django.utils import timezone
from asapp.models import User, Tag, Thread, Message, Report
import uuid

users = [
    User(uid="user1", displayname="John Doe", pronouns="he/him", permissions=1),
    User(uid="user2", displayname="Jane Smith", pronouns="she/her", permissions=4),
    User(uid="user3", displayname="Alex Johnson", pronouns="they/them", permissions=2),
]

User.objects.bulk_create(users)

tags = [
    Tag(name="Calc"),
    Tag(name="CCI"),
    Tag(name="API"),
]

Tag.objects.bulk_create(tags)

threads = [
    Thread(title="How to find the derivative of...", author=users[0], date=timezone.now()),
    Thread(title="My thread titel", author=users[1], date=timezone.now()),
]

Thread.objects.bulk_create(threads)
threads[0].tags.add(tags[1]) 
threads[1].tags.add(tags[1], tags[2]) 

messages = [
    Message(thread=threads[0], author=users[0], date=timezone.now(), body="Here is how to...", votes=5),
    Message(thread=threads[1], author=users[1], date=timezone.now(), body="This is a thread body content", votes=3),
]

Message.objects.bulk_create(messages)


reports = [
    Report(message=messages[0], author=users[1], date=timezone.now(), reason="This is a test report", comment="Please check the content"),
]

Report.objects.bulk_create(reports)
