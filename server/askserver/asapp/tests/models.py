from django.utils import timezone
from django.test import TestCase
from asapp.models import Thread, Message, Tag, Report, User

from rest_framework.authtoken.models import Token

class APITestCase(TestCase):
    def setUp(self):
        
        self.user_admin   = User.objects.create_user(uid='meiwang1',
            password='insecurePassword', permissions=4)
        self.user_admin_token = Token.objects.create(user=self.user_admin)
        self.user_admin.displayname = 'TWVpbGkgV2FuZyAo546L576O5Li9KQ'
        self.user_admin.pronouns = 'emllL2hpcg'

        self.user_ta_ia = User.objects.create_user(uid='sorudai0', 
            password='insecurePassword', permissions=2)
        self.user_ta_ia_token = Token.objects.create(user=self.user_ta_ia)
        self.user_ta_ia.displayname = 'U2XDoW4gw5MgUnVkYcOt'
        self.user_ta_ia.pronouns = 'dGhleS90aGVt'
        
        self.user_regular = User.objects.create_user(uid='josmith8',
            password='insecurePassword', permissions=1)
        self.user_regular_token = Token.objects.create(user=self.user_regular)
        self.user_regular.displayname = 'Sm9obiBTbWl0aA'
        self.user_regular.pronouns = 'aGUvaGlt'

        
        
        self.tag1 = Tag.objects.create(name="Python")
        self.tag2 = Tag.objects.create(name="Java")
        self.tag2 = Tag.objects.create(name="Cpp")


        
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
