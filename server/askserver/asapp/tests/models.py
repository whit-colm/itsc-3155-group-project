from django.utils import timezone
from django.test import TestCase
from asapp.models import Thread, Message, Tag, Report, User
from asapp.b64url_enhancement import *
import uuid

from rest_framework.authtoken.models import Token

class TestTag(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create("Python")

    def test_create_duplicates(self):
        pass

    def test_delete(self):
        pass

    def test_delete_noexist(self):
        pass

class TestUser(TestCase):
    def setUp(self):
        
        self.uid = 'myuid'
        self.user   = User.objects.create_user(uid=self.uid,
            password='insecurePassword', permissions=4)
        self.user = Token.objects.create(user=self.user)
        self.user.displayname = 'TWVpbGkgV2FuZyAo546L576O5Li9KQ'
        self.user.pronouns = 'emllL2hpcg'
        
        self.tag = Tag.objects.create(name="Python")

    def test_render_str(self):
        assertEqual(self.uid, str(self.user))

    def test_created_thread(self):
        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
            tags=["Python"]
        )

        Message.objects.create(
            author=self.user,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

    def test_authored_threads(self):
        pass

    def test_follow_tags(self):
        # Test following a tag and getting that for the profile
        pass

    def test_follow_tags_nonexistent(self):
        # test following a tag that does not exist
        pass

    def test_follow_tags_delted(self):
        # test following a tag that is then deleted
        pass


class TestThread(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(uid='meiwang1',
            password='insecurePassword', permissions=4)
        self.user_token = Token.objects.create(user=self.user)
        self.user.displayname = 'TWVpbGkgV2FuZyAo546L576O5Li9KQ'
        self.user.pronouns = 'emllL2hpcg'
        
        self.uuid=uuid.UUID(int=0x1)
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            id=self.uuid,
            title=b64url_encode_str("Test Thread"),
            anonymous=False,
            tags=["Python"]
        )

        Message.objects.create(
            author=self.user,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )
    
    def test_str(self):
        # test the custom __str__() method
        self.assertEqual(str(self.thread.id), str(self.thread))

    def test_as_api(self):
        # Test the as_api() method
        pass

    def test_tag_nonexistent(self):
        # Test creating a thread with tags that do not exist
        pass

    def test_no_tags(self):
        # Test creating a thread with no tags
        pass

    def test_tags_deleted(self):
        # Test creating a thread with multiple tags, one of which gets deleted
        pass

    def test_tag_deleted(self):
        # Test creating a thread with a single tag which gets deleted
        pass

    def test_award(self):
        # Test giving a message an award
        pass

    def test_award_question(self):
        # Test giving an award to the question message
        pass

    def test_award_deadmessage(self):
        # Test giving an award to the "dead" message
        pass

    def test_award_thendead(self):
        # Test giving an award to a message which is then "killed"abs
        pass

    def test_award_hidden(self):
        # Test giving an award to a hidden message
        pass

    def test_award_thenhide(self):
        # Test giving an award to a message, then hiding the message
        pass

    def test_award_different_thread(self):
        # Test giving an award to a message on a different thread
        pass

class TestMessage(TestCase):
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

        
        
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
            tags=["Python"]
        )

        Message.objects.create(
            author=self.user_regular,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

    def test_create(self):
        # Test creating a message in a thread
        pass

    def test_create_in_nonexistent_thread(self):
        # Test creating a message in a thread that does not exist
        pass

    def test_create_second_questionmessage(self):
        # Test creating second question message
        pass

    def test_create_no_body(self):
        # Test creating a message with no body
        pass

    def test_create_reply(self):
        # Test creating a message with a reply
        pass

    def test_create_reply_different_thread(self):
        # Test creating a message in one thread which replies to a message in a
        # different thread
        pass

    def test_create_reply_deadmessage(self):
        # Test creating a message which replies to the "dead" message
        pass

    def test_create_reply_thendead(self):
        # Test creating a reply to a message which is then deleted (i.e. dead)
        pass


class TestReport(TestCase):
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

        
        
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
            tags=["Python"]
        )

        Message.objects.create(
            author=self.user_regular,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

    def test_create(self):
        # Test creating a report
        pass

    def test_create_without_reason(self):
        # Test creating a report without a reason
        pass

    def test_create_with_nonexistent_message(self):
        # Test creating a report without a valid message
        pass