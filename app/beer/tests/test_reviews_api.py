from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Review

from beer.serializers import ReviewSerializer


REVIEWS_URL = reverse("beer:review-list")


class PublicReviewsApiTests(TestCase):
    """Test the publically available reviews API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(REVIEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewsAPITests(TestCase):
    """Test reviews can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@londonappdev.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_review_list(self):
        """Test retrieving a list of reviews"""
        Review.objects.create(
            user=self.user, name="Castle", aroma=3, appearance=2, taste=1
        )
        Review.objects.create(
            user=self.user, name="Windhoek", aroma=3, appearance=2, taste=1
        )

        res = self.client.get(REVIEWS_URL)

        reviews = Review.objects.all().order_by("-name")
        serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_reviews_limited_to_user(self):
        """Test that only reviews for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            "other@londonappdev.com", "testpass"
        )
        Review.objects.create(
            user=user2, name="Budweiser", aroma=3, appearance=2, taste=1
        )

        review = Review.objects.create(
            user=self.user, name="Coors", aroma=3, appearance=2, taste=1
        )

        res = self.client.get(REVIEWS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], review.name)
