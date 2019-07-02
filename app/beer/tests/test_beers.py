from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Beer

from beer.serializers import BeerSerializer


BEERS_URL = reverse("beer:beer-list")


class PublicBeersApiTests(TestCase):
    """Test the publically available beers API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(BEERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBeersAPITests(TestCase):
    """Test beers can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@johangenis.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_beer_list(self):
        """Test retrieving a list of beers"""
        Beer.objects.create(user=self.user, name="Guiness")
        Beer.objects.create(user=self.user, name="Coors")

        res = self.client.get(BEERS_URL)

        beers = Beer.objects.all().order_by("-name")
        serializer = BeerSerializer(beers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_beers_limited_to_user(self):
        """Test that only beers for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            "other@johangenis.com", "testpass"
        )
        Beer.objects.create(user=user2, name="Budweiser")

        beer = Beer.objects.create(user=self.user, name="Hansa")

        res = self.client.get(BEERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], beer.name)
