from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Beer

from beer.serializers import BeerSerializer


BEERS_URL = reverse("beer:beer-list")


def sample_beer(user, **params):
    """Create and return a sample beer"""
    defaults = {
        "name": "Sample Beer",
        "ibu": 54,
        "calories": 500,
        "abv": 10,
        "style": "Strong",
        "brewery_location": "Cape Town",
    }
    defaults.update(params)
    return Beer.objects.create(user=user, **defaults)


# def detail_url(beer_id):
#     """Return beer detail url"""
#     return reverse("beer:beer-detail", args=[beer_id])


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
        sample_beer(user=self.user)
        sample_beer(user=self.user)

        res = self.client.get(BEERS_URL)

        beers = Beer.objects.all().order_by("-id")
        serializer = BeerSerializer(beers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_beers_limited_to_user(self):
        """Test that only beers for authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            "other@johangenis.com", "testpass"
        )
        sample_beer(user=user2)
        sample_beer(user=self.user)

        res = self.client.get(BEERS_URL)
        beer = Beer.objects.filter(user=self.user)
        serializer = BeerSerializer(beer, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_beer_successful(self):
        """Test creating a new beer"""
        payload = {
            "name": "Hansa",
            "ibu": "5",
            "calories": "600",
            "abv": "4.5",
            "style": "bitter",
            "brewery_location": "South Africa",
        }
        self.client.post(BEERS_URL, payload)

        exists = Beer.objects.filter(
            user=self.user, name=payload["name"]
        ).exists()
        self.assertTrue(exists)

    def test_create_beer_invalid(self):
        """Test creating invalid beer fails"""
        payload = {"name": ""}
        res = self.client.post(BEERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_view_beer_detail(self):
    #     """Test viewing a beer's detail"""
    #     beer = sample_beer(user=self.user)
    #     # beer.review.add(sample_review(user=self.user))
    #
    #     url = detail_url(beer.id)
    #     res = self.client.get(url)
    #
    #     serializer = BeerDetailSerlializer(beer)
    #     self.assertEqual(res.data, serializer.data)
