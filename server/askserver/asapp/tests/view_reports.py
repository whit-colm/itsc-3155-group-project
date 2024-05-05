from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase
from asapp.models import User, Tag, Message, Thread, Report, ReportTag
from asapp.views.reports import *
from asapp.b64url_enhancement import b64url_decode_str, b64url_encode_str
from rest_framework.authtoken.models import Token
import json

class POST_reports_new__TestCase(TestCase):
    def setUp(self):
        # this is an ugly way to do this, but the report tags
        # are hard baked into the system.
        ReportTag.objects.get_or_create(name="Suspected violation of academic integrity")
        ReportTag.objects.get_or_create(name="Offensive or inappropriate behavior")
        ReportTag.objects.get_or_create(name="Hate speech")
        ReportTag.objects.get_or_create(name="Spam")
        ReportTag.objects.get_or_create(name="Promotion of illegal activities")
        ReportTag.objects.get_or_create(name="Something else")

        self.factory = APIRequestFactory()
        
        self.user_reporter = User.objects.create_user(uid='josmith8',
            password='insecurePassword', permissions=1)
        self.user_reporter_token = Token.objects.create(user=self.user_reporter)
        self.user_reporter.displayname = 'Sm9obiBTbWl0aA'
        self.user_reporter.pronouns = 'aGUvaGlt'
        self.user_reporter.save()

        self.user_reported = User.objects.create_user(uid='emuster2',
            password='insecurePassword', permissions=1)
        self.user_reported_token = Token.objects.create(user=self.user_reported)
        self.user_reported.displayname = 'RXJpa2EgTXVzdGVybWFubg'
        self.user_reported.pronouns = 'c2hlL2hlcg'
        self.user_reported.save()
        
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
        )
        self.thread.tags.set([self.tag])

        Message.objects.create(
            author=self.user_reporter,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

        self.offending_message = Message.objects.create(
            author=self.user_reported,
            thread=self.thread,
            body=b64url_encode_str("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
            question=False
        )

    def test_create(self):
        # Create a Report
        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Suspected violation of academic integrity"
            ],
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        response_json = json.loads(response.content.decode('utf-8'))
        db_report = Report.objects.get(id=response_json['report']['id'])
        self.assertEqual(200, response.status_code)

        self.assertEqual(db_report.as_api(), response_json['report'])
        self.assertEqual(str(self.user_reported), response_json['report']['message']['author']['uid'])

    def test_create_with_nonexistent_message(self):
        # Create a report without a message
        reportData = {
            "reason": [
                "Suspected violation of academic integrity"
            ],
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        self.assertEqual(400, response.status_code)

        

    def test_create_with_invalid_message(self):
        # Create a report where the message does not exist
        bogus_id = uuid.uuid4()

        reportData = {
            "messageID": str(bogus_id),
            "reason": [
                "Suspected violation of academic integrity"
            ],
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        self.assertEqual(404, response.status_code)
        
        self.assertEqual(Report.objects.filter(message=bogus_id).first(), None)

    def test_create_without_base64(self):
        # Create a report without urlsafe base64 in the message field
        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Suspected violation of academic integrity"
            ],
            "comment": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        self.assertEqual(400, response.status_code)

    def test_create_with_nonexistent_tags(self):
        # Create a report without tags
        reportData = {
            "messageID": str(self.offending_message),
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        self.assertEqual(400, response.status_code)

    def test_create_with_invalid_tags(self):
        # Create a report with tags that do not exist
        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Guess who just got kicked out of starbucks for",
                "You guessed it",
                "Being white."
            ],
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        # Create the request
        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter_token}'

        # Execute endpoint
        response = reports_new(request)

        # Test DB queries against API structure
        self.assertEqual(400, response.status_code)

class GET_reports__TestCase(TestCase):
    def setUp(self):
        # this is an ugly way to do this, but the report tags
        # are hard baked into the system.
        ReportTag.objects.get_or_create(name="Suspected violation of academic integrity")
        ReportTag.objects.get_or_create(name="Offensive or inappropriate behavior")
        ReportTag.objects.get_or_create(name="Hate speech")
        ReportTag.objects.get_or_create(name="Spam")
        ReportTag.objects.get_or_create(name="Promotion of illegal activities")
        ReportTag.objects.get_or_create(name="Something else")

        self.factory = APIRequestFactory()

        self.user_admin = User.objects.create_user(uid='meiwang1',
            password='insecurePassword', permissions=4)
        self.user_admin_token = Token.objects.create(user=self.user_admin)
        self.user_admin.displayname = 'TWVpbGkgV2FuZyAo546L576O5Li9KQ'
        self.user_admin.pronouns = 'emllL2hpcg'
        self.user_admin.save()

        self.user_ta_ia = User.objects.create_user(uid='sorudai0', 
            password='insecurePassword', permissions=2)
        self.user_ta_ia_token = Token.objects.create(user=self.user_ta_ia)
        self.user_ta_ia.displayname = 'U2XDoW4gw5MgUnVkYcOt'
        self.user_ta_ia.pronouns = 'dGhleS90aGVt'
        self.user_ta_ia.save()

        self.user_reported = User.objects.create_user(uid='emuster2',
            password='insecurePassword', permissions=1)
        self.user_reported_token = Token.objects.create(user=self.user_reported)
        self.user_reported.displayname = 'RXJpa2EgTXVzdGVybWFubg'
        self.user_reported.pronouns = 'c2hlL2hlcg'
        self.user_reported.save()
        
        self.user_reporter1 = User.objects.create_user(uid='josmith8',
            password='insecurePassword', permissions=1)
        self.user_reporter1_token = Token.objects.create(user=self.user_reporter1)
        self.user_reporter1.displayname = 'Sm9obiBTbWl0aA'
        self.user_reporter1.pronouns = 'aGUvaGlt'
        self.user_reporter1.save()

        self.user_reporter2 = User.objects.create_user(uid='jperez4',
            password='insecurePassword', permissions=1)
        self.user_reporter2_token = Token.objects.create(user=self.user_reporter2)
        self.user_reporter2.displayname = 'SnVhbiBQw6lyZXo'
        self.user_reporter2.save()
        
        self.tag = Tag.objects.create(name="Python")

        self.thread = Thread.objects.create(
            title=b64url_encode_str("Test Thread"), 
        )
        self.thread.tags.set([self.tag])

        Message.objects.create(
            author=self.user_reporter1,
            thread=self.thread,
            body=b64url_encode_str("Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed congue auctor elit, sit amet cursus lectus sodales ut. Sed ut tempor lectus, sed pharetra lacus. Maecenas ultrices, nulla id vehicula faucibus, est enim convallis sem, nec feugiat eros risus a sem. Fusce rhoncus turpis ut ultricies fermentum. Nam dapibus dolor justo, vel tempor lorem bibendum vel. Ut dapibus ultrices lorem, sed fermentum est ultricies nec. Integer suscipit euismod tellus nec lobortis. Vestibulum suscipit efficitur felis, eget finibus enim fringilla sed. Morbi tincidunt, risus eget luctus suscipit, neque nunc ullamcorper velit, a commodo dui odio nec velit. Cras nec orci nec odio fermentum commodo."),
            question=True
        )

        self.offending_message = Message.objects.create(
            author=self.user_reported,
            thread=self.thread,
            body=b64url_encode_str("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
            question=False
        )

        ### Now report the same message a bunch. ###
        # 1
        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Suspected violation of academic integrity"
            ],
            "comment": "RG9uZWMgdWx0cmljZXMgYXJjdSBhIHRlbGx1cyBmZXJtZW50dW0gcHVsdmluYXIuIEFsaXF1YW0gbW9sZXN0aWUgYSBudW5jIHZpdGFlIHRpbmNpZHVudC4g"
        }

        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter1_token}'
        reports_new(request)

        # 2

        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Offensive or inappropriate behavior"
            ],
            "comment": "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZy4gVGhpcyBzZW50ZW5jZSBjb250YWlucyBldmVyeSBsZXR0ZXIgb2YgdGhlIGFscGhhYmV0Lg"
        }

        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter2_token}'
        reports_new(request)

        # 3

        reportData = {
            "messageID": str(self.offending_message),
            "reason": [
                "Hate speech"
            ],
            "comment": "S2EgdGFrYSB0ZSByxIEga2kgdGUgd2hlbnVhLCBrYSBoaW5nYSB0ZSBrxY1oYXR1IGtpIHRlIHdhaS4"
        }

        request = self.factory.post(
            path='/reports/new/',
            data = reportData,
            format='json',
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_ta_ia_token}'
        reports_new(request)

    def test_get(self):
        # Get Reports
        # Create the request
        request = self.factory.get(
            path='/reports/',
            format='json'
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_admin_token}'

        # Execute endpoint
        response = reports(request)
        # Test DB queries against API structure
        response_json = json.loads(response.content.decode('utf-8'))
        #db_report = Report.objects.get(id=response_json['report']['id'])
        self.assertEqual(200, response.status_code)

        self.assertEqual(3, len(response_json['reports']))

    def test_get_unperm(self):
        # Get Reports
        # Create the request
        request = self.factory.get(
            path='/reports/',
            format='json'
        )
        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_ta_ia_token}'

        # Execute endpoint
        response = reports(request)
        # Test DB queries against API structure
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(403, response.status_code)

        request.META['HTTP_AUTHORIZATION'] = f'Token {self.user_reporter2_token}'
        response = reports(request)
        self.assertEqual(403, response.status_code)