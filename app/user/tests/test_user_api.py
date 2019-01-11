from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Creates a user in our DB"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the UserAPI Public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test if user with valid payload is successful"""
        payload = {
            'email': 'test1@test.com',
            'password': 'testPass',
            'name': 'Jimmychoo'
        }

        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', resp.data)

    def test_user_already_exists(self):
        """Test that create user fails if they already exist"""
        payload = {
            'email': 'test1@test.com',
            'password': 'testPass',
            'name': 'Jimmychoo'
        }
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test1@test.com',
            'password': 'pw',
            'name': 'Jimmychoo'
        }

        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """Test that the token is created for user"""
        payload = {'email': 'test@test.com', 'password': 'TestPass'}
        create_user(**payload)

        resp = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com', password="TestPass")
        payload = {'email': 'test@test.com', 'password': 'TestPASS'}
        resp = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': 'TestPASS'}
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that token is not created if not password is given"""
        payload = {'email': 'test@test.com', 'password': ''}
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
