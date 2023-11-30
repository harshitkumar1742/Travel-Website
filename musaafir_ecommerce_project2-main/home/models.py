from django.db import models
from django.contrib.auth.models import User 
from django.db.models import Avg, Count
from django.core.validators import *
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="customer", null=True, blank=True)
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)
    company_name = models.CharField(max_length=200, default=None, null=True)
    budget = models.IntegerField(default=0, null=True, blank=True)
    updated_budget = models.IntegerField(default=0, null=True, blank=True)
    total_budget = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.name

class CityCab(models.Model):
    CITY = [
        ('Mumbai', 'Mumbai'),
        ('Pune', 'Pune'),
        ('Navi Mumbai', 'Navi Mumbai')
    ]

    CAR_TYPE = [

        ('Hatchbacks & sedans', 'Hatchbacks & sedans'),
        ('SUV', 'SUV'),
        ('Tempo travellers', 'Tempo travellers')

    ]

    PASSENGER_COUNT = [

        ('1-4', '1-4'),
        ('4-7', '4-7'),
        ('7-16', '7-16')

    ]

    
    HOURLY_PACKAGE = [

        ('3 hours', '30'),
        ('6 hours', '60'),
        ('15 hours', '150')

    ]

    CAR_OPTION = [

        ('CITY COMMUTE', 'CITY COMMUTE'),
        ('OUTSTATION', 'OUTSTATION'),
        ('RENTAL', 'RENTAL')


    ]

    car_type = models.CharField(max_length=20, null=True, blank= True, choices = CAR_TYPE)
    car_option = models.CharField(max_length=50, null=True, blank= True, choices = CAR_OPTION)
    name=models.CharField(max_length=200, null=True, blank=True)
    price=models.FloatField(default=0)
    pickup_city = models.CharField(default = None, max_length=20, null=True, blank= True, choices = CITY)
    drop_city = models.CharField(default = None, max_length=20, null=True, blank= True, choices = CITY)
    no_of_passengers = models.CharField(max_length=5, null=True, blank= True,  choices = PASSENGER_COUNT)
    categoryname=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)
    description=models.CharField(max_length=1000, null=True, blank= True)
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    driver_contact = models.CharField(max_length=12, null=True, blank=True)
    is_available = models.BooleanField(default=True)


    def __str__(self):
        return str(self.name)

        #in case there is no image url associated with the product, our server should not return an error. 
    def imageurl(self):
        try: 
            url=self.image.url
        except:
            url=''
        return url


class CityCabBooking(models.Model):

    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    cabname=models.ForeignKey(CityCab, on_delete=models.SET_NULL, null=True, blank=True)
    pickup=models.CharField(max_length=200, null=True, blank=True)
    pickup_datetime=models.CharField(max_length=200, null=True, blank= True)
    destination=models.CharField(max_length=200, null=True, blank=True)
    price=models.FloatField(default=0)
    payment_done=models.BooleanField(default=False)
    can_cancel = models.BooleanField(default=True)
    



    def __str__(self):
        return str(self.customer)


class CityCab_Reviews(models.Model):

    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name =models.ForeignKey(CityCab, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    review=models.TextField(max_length=250, null=True, blank=True)
    rate=models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return str(self.customer)

    
    def rate_total(self):
        total=0
        for rate in self.rate:
            total +=rate 
        return total

