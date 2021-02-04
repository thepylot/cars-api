import requests
from django.db.models import Sum

from rest_framework import serializers
from core.models import Car, Rate

CAR_MAKE_API = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
CAR_MODEL_API = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json'


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('car', 'rate',)
        read_only_fields = ('id',)

    def validate_rate(self, rate):
        """Check that rate value is between 1-5"""
        if not 0 <= rate <= 5:
            raise serializers.ValidationError("Rate value must between 1-5")
        return rate


class CarSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField('get_avg_rate')

    class Meta:
        model = Car
        fields = ('make_name', 'model_name', 'rate',)
        read_only_fields = ('id',)

    def get_avg_rate(self, car):
        """ Get average rate value for particular car object"""
        rates = Rate.objects.filter(car_id=car.id)
        if rates:
            return round(rates.aggregate(Sum('rate'))['rate__sum'] / len(rates))
        else:
            return 0

    def validate_make_name(self, make_name):
        res = requests.get(CAR_MAKE_API).json()
        try:
            car_make = next(item for item in res['Results'] 
                                if item["Make_Name"] == make_name.upper())
        except StopIteration:
            raise serializers.ValidationError("Requested Car Make Not Found.")
        return car_make['Make_Name']

    def validate_model_name(self, model_name):
        res = requests.get(CAR_MODEL_API.format(self.initial_data.get("make_name").upper())).json()
        try:
            car_model = next(item for item in res['Results'] 
                                if item["Model_Name"] == model_name)
        except StopIteration:
            raise serializers.ValidationError("Requested Car Model Not Found.")
        return car_model['Model_Name']


class PopularCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('make_name', 'model_name',)
        read_only_fields = ('id',)