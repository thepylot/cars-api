from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics

from core.models import Car, Rate
from car import serializers


class CarViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage cars in database"""
    queryset = Car.objects.all()
    serializer_class = serializers.CarSerializer

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save()


class RateViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """Manage rates in database"""
    queryset = Rate.objects.all()
    serializer_class = serializers.RateSerializer

    def get_queryset(self):
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        serializer.save()


class PopularCarViewSet(viewsets.GenericViewSet, 
                        generics.ListAPIView):
    """Manage popular cars in database"""
    serializer_class = serializers.PopularCarSerializer

    def get_queryset(self):
        ordered_queryset = Rate.objects.values('car').annotate(total_rates=Count('car')).order_by('-total_rates')
        return [get_object_or_404(Car, id=item['car']) for item in ordered_queryset]
