from django.test import TestCase
from core import models


class ModelTests(TestCase):

    def test_car_str(self):
        """Test the car string representation"""
        car = models.Car.objects.create(
            make_name='HONDA',
            model_name='Accord',
        )

        self.assertEqual(str(car), f"{car.make_name}-{car.model_name}")

    def test_rate_str(self):
        """Test the rate string representation"""
        car = models.Car.objects.create(
            make_name='HONDA',
            model_name='Accord',
        )

        rate = models.Rate.objects.create(
            car=car,
            rate=4
        )

        self.assertEqual(str(rate), rate.car.model_name)