from django.utils import timezone
from django.test import TestCase
from asapp.models import Thread, Message, Tag, Report, User

class APITestCase(TestCase):
    def setUp(self):
        
        self.user_admin = User.objects.create_user(uid='admin1', password='pass', permissions=5)
        self.user_regular = User.objects.create_user(uid='user1', password='pass', permissions=1)
        
        
        self.tag1 = Tag.objects.create(name="Python")
        self.tag2 = Tag.objects.create(name="Django")

        
        self.thread = Thread.objects.create(title="Test Thread", author=self.user_admin, date=timezone.now())
        self.message = Message.objects.create(thread=self.thread, author=self.user_admin, body="Hello World", date=timezone.now())
        self.report = Report.objects.create(message=self.message, author=self.user_regular, reason="Spam", comment="Test Comment", date=timezone.now())

    def test_get_user_profile(self):
        self.client.login(username='admin1', password='pass')
        response = self.client.get('/objs/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("admin1", response.content.decode())

    def test_create_tag_with_low_permission(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/objs/tags/new/', {'tag': 'Flask'})
        self.assertEqual(response.status_code, 403)  

    def test_create_tag_with_high_permission(self):
        self.client.login(username='admin1', password='pass')
        response = self.client.post('/objs/tags/new/', {'tag': 'Flask'})
        self.assertEqual(response.status_code, 200)
