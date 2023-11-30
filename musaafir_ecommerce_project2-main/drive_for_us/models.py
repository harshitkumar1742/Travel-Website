from django.db import models
from home.models import User 


class NeedCar(models.Model):
    name=models.TextField(max_length=50)
    phone_number = models.CharField(max_length=12)
    city= models.TextField(max_length=50)

    def __str__(self):
        return self.name

class AttachCar(models.Model):

    CAR_TYPE = [

        ('Hatchbacks and sedans', 'Hatchbacks and sedans'),
        ('SUV', 'SUV'),
        ('Tempo travellers', 'Tempo travellers')

    ]

    name=models.TextField(max_length=50)
    phone_number = models.CharField(max_length=12)
    city= models.TextField(max_length=50)
    car_type = models.CharField(max_length=50, null=True, blank= True, choices = CAR_TYPE)

    def __str__(self):
        return self.name


    




