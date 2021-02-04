import requests
from django.urls import reverse
from django.test import TestCase
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Car, Rate

from car.serializers import CarSerializer, PopularCarSerializer

CAR_URL = reverse('car:cars-list')
POPULAR_CAR_URL = reverse('car:popular-list')

CAR_MAKE_EXTERNAL_API = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
CAR_MODEL_EXTERNAL_API = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json'


def sample_car(**params):
    """Create and return a sample car"""
    defaults = {
        'make_name': 'HONDA',
        'model_name': 'Accord',
    }
    defaults.update(params)

    return Car.objects.create(**defaults)


class PublicCarApiTests(TestCase):
    """Test the publicly available cars API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_car_list(self):
        """Test retriving a list of cars"""
        sample_car()
        sample_car()

        res = self.client.get(CAR_URL)

        cars = Car.objects.all().order_by('-make_name')
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_car_successful(self):
        """Test a new car creation was successful by checking External API"""
        payload = {
            'make_name': 'ASTON MARTIN',
            'model_name': 'V8 Vantage',
        }

        self.client.post(CAR_URL, payload)

        exists = Car.objects.filter(
            make_name=payload['make_name'],
            model_name=payload['model_name']
        ).exists()

        self.assertTrue(exists)

    def test_create_car_with_lowercase(self):
        """Test a new car creation with lowercase"""
        payload = {
            'make_name': 'aston martin',
            'model_name': 'V8 Vantage',
        }
        res = self.client.post(CAR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_car_invalid(self):
        """Test a new car creation failed"""
        payload = {'model_name': ''}
        res = self.client.post(CAR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_car_average_rate_value(self):
        """Test average rate value for particular car"""
        car = sample_car()

        Rate.objects.create(car=car, rate=3)
        Rate.objects.create(car=car, rate=5)

        res = self.client.get(CAR_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['rating'], 4)
    
    def test_car_default_rate_value(self):
        """Test default rate value for particular car"""
        sample_car()
        res = self.client.get(CAR_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['rating'], 0)

    def test_retrieve_popular_cars(self):
        """Test retrieve popular cars based on number of rates"""
        car1 = sample_car(make_name="BMW", model_name="M4")
        car2 = sample_car(make_name="Mercedes", model_name="Benz")

        Rate.objects.create(car=car1, rate=4)
        Rate.objects.create(car=car1, rate=2)
        Rate.objects.create(car=car1, rate=2)
        Rate.objects.create(car=car2, rate=3)
        Rate.objects.create(car=car2, rate=5)

        res = self.client.get(POPULAR_CAR_URL)

        ordered_queryset = Rate.objects.filter(car_id=car1.id).values('car').annotate(total_rates=Count('car'))
        popular_cars = [get_object_or_404(Car, id=item['car']) for item in ordered_queryset]
        serializer = PopularCarSerializer(popular_cars, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializer.data[0])


class ExternalCarApiTests(TestCase):
    """ Test for External Vehicle API"""

    def setUp(self):
        self.client = APIClient()

    def test_car_in_vehicles(self):
        """Test requested car exists inside the external API data"""
        payload = {
            'make_name': 'ASTON MARTIN',
            'model_name': 'V8 Vantage',
        }

        car_makes_res = requests.get(CAR_MAKE_EXTERNAL_API).json()
        car_make = next(item for item in car_makes_res['Results'] if item["Make_Name"] == payload['make_name'])

        if car_make:
            car_models_res = requests.get(CAR_MODEL_EXTERNAL_API.format(car_make['Make_Name'])).json()
            car_model = next(item for item in car_models_res['Results']
                                     if item["Model_Name"] == payload['model_name'])

            self.assertIn(car_model['Make_Name'], payload['make_name'])

    def test_car_not_in_vehicles(self):
        """Test requested car DO NOT exists inside the external API data"""
        payload = {
            'make_name': 'Test Make',
            'model_name': 'Test Model',
        }

        car_makes_res = requests.get(CAR_MAKE_EXTERNAL_API).json()
        try:
            car_make = next(item for item in car_makes_res['Results'] 
                                    if item["Make_Name"] == payload['make_name'])
        except StopIteration:
            return None

        self.assertEqual(car_make, None)