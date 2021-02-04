from django.urls import path, include
from rest_framework.routers import DefaultRouter

from car import views

router = DefaultRouter()
router.register('cars', views.CarViewSet, basename='cars')
router.register('rate', views.RateViewSet, basename='rate')
router.register('popular', views.PopularCarViewSet, basename='popular')


app_name = 'car'

urlpatterns = [
    path('', include(router.urls))
    ]