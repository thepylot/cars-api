from django.db import models


class Car(models.Model):
    make_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.make_name}-{self.model_name}"


class Rate(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='car')
    rate = models.IntegerField()

    def __str__(self):
        return self.car.model_name