from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.test import TestCase
from asapp.models import User, Tag, Thread
from rest_framework.authtoken.models import Token

from rest_framework.test import APIRequestFactory

class ObjsViewTestCase(TestCase):
    def setUp(self):
        # Set necessary configuration for these tests
        pass

    def test_GET_objs_profile(self):
        # Test GET /objs/profile
        pass