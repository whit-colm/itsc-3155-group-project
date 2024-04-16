
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from askserver.models import User, Tag, Thread
from django.utils import timezone

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_admin = User.objects.create_user(uid="admin", permissions=4, password='password123')
        self.regular_user = User.objects.create_user(uid="regular", permissions=1, password='password')
        self.user_guest = User.objects.create_user(uid="guest", permissions=0, password='pass')
        

        self.tag_url = reverse('create_tag')  
        self.thread_url = reverse('create_thread')  

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_tag_admin(self):
        self.authenticate(self.user_admin)
        response = self.client.post(self.tag_url, {'tag': 'NewTag'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tag_guest_forbidden(self):
        self.authenticate(self.user_guest)
        response = self.client.post(self.tag_url, {'tag': 'NewTag'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_thread_admin(self):
        self.authenticate(self.user_admin)
        response = self.client.post(self.thread_url, {
            'title': 'Example Thread',
            'body': 'This is a sample thread.',
            'tags': ['Django', 'API'],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_thread_guest(self):
        self.authenticate(self.user_guest)
        response = self.client.post(self.thread_url, {
            'title': 'Example Thread',
            'body': 'This is a sample thread.',
            'tags': ['Django', 'API'],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
