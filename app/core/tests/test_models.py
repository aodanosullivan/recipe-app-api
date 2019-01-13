from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def test_create_new_user_with_email_successful(self):
        '''Test creating a new user with email is successful'''

        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, password)

    def test_new_user_email_normalized(self):
        """Test that the new user email is normalized"""
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'TESTSET')

        self.assertEqual(user.email, email.lower())

    def test_new_user_no_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "TEST")

    def test_create_superuser(self):
        """Test creating super user"""
        user = get_user_model().objects.create_superuser(
            "test@test.com",
            "test")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
