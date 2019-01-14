from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """Test the publically available Tags"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is needed to get tags"""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test the authorized user API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving Tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Desert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that the tags are limited to the user logged in"""

        self.user2 = get_user_model().objects.create_user(
            'test@test2.com',
            'testPass'
        )

        Tag.objects.create(user=self.user2, name='Fruity')

        tag = Tag.objects.create(user=self.user, name="Comfort Food")
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""

        payload = {'name': 'TestTag'}
        self.client.post(TAGS_URL, payload)

        tag = Tag.objects.filter(user=self.user,
                                 name=payload['name']).exists()
        self.assertTrue(tag)

    def test_tag_must_be_valid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
