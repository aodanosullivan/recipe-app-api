from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


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

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Onion'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_converting_recipe_to_string(self):
        """Test converting recipe string representation"""

        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Steak & mushroom sauce",
            time_minutes=5,
            price=5.00)

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """Test the image is saved in the correct location"""

        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, expected_path)
