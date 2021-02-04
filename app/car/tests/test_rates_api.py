from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Rate

from car.tests.test_cars_api import sample_car

RATE_URL = reverse('car:rate-list')


class PublicRateApiTests(TestCase):
    """Test the publicly available rate API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_rate_successful(self):
        """Test a new rate creation successful"""
        payload = {"car": sample_car(), "rate": 4}

        self.client.post(RATE_URL, payload)

        exists = Rate.objects.filter(
            car=payload['car']
        ).exists

        self.assertTrue(exists)

    def test_create_rate_invalid(self):
        """Test a new rate creation failed"""
        payload = {"car": None, "rate": 4}

        res = self.client.post(RATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_value_validation(self):
        """Test validation rate is between 1-5"""
        payload = {
            "car": sample_car(),
            "rate": 7
        }

        res = self.client.post(RATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)