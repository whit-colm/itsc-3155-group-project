from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase
from asapp.models import User, Tag, Thread
from asapp.b64url_enhancement import b64url_decode_str, b64url_encode_str
from rest_framework.authtoken.models import Token

class ReportsViewTestCase(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(uid='meiwang1',
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
        
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
        )
        self.thread.tags.set(["Python"])

        Message.objects.create(
            author=self.user_regular,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

    def create(self):
        # Create a Report
        

        pass
