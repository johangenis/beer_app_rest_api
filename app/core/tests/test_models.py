from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@johangenis.com", password="Test123"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@johangenis.com"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@JOHANGENIS.com"
        user = get_user_model().objects.create_user(email, "Test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Test123")

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@johangenis.com", "Test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name="Lager")

        self.assertEqual(str(tag), tag.name)

    def test_beer_str(self):
        """Test the beer string representation"""
        beer = models.Beer.objects.create(
            user=sample_user(), name="Castle Lager"
        )

        self.assertEqual(str(beer), beer.name)

    def test_review_str(self):
        """Test the review string representation"""
        review = models.Review.objects.create(
            user=sample_user(), name="Castle Light"
        )

        self.assertEqual(str(review), review.name)
