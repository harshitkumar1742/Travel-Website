from django.db import models
from home.models import User, Customer
from django.contrib.auth.models import AbstractUser


class ContactUs(models.Model):

    CITY = [
        ('Mumbai', 'Mumbai'),
        ('Pune', 'Pune'),
        ('Navi Mumbai', 'Navi Mumbai')
    ]
    name=models.TextField(max_length=80)
    email=models.EmailField(max_length=100)
    company_name = models.TextField(max_length=80)
    phone_number = models.CharField(max_length=12)
    city= models.TextField(max_length=50, choices = CITY)
    comments=models.TextField(max_length=500)

    def __str__(self):
        return self.company_name

class AddEmployees(models.Model):
    name=models.TextField(max_length=80, null=True, blank=True)
    email=models.EmailField(max_length=100, null=True, blank=True)
    company_name = models.TextField(max_length=80, null=True, blank=True)
    budget = models.IntegerField(default=0, null=True, blank=True)
    updated_budget = models.IntegerField(default=0, null=True, blank=True)
    total_budget = models.IntegerField(default=0, null=True, blank=True)
    payment_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.company_name


class CompanySignUp(models.Model):
    CITY = [
        ('Mumbai', 'Mumbai'),
        ('Pune', 'Pune'),
        ('Navi Mumbai', 'Navi Mumbai')
    ]
    name = models.TextField(max_length=80, null=True, blank=True) 
    company_name = models.TextField(max_length=80, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    city= models.TextField(max_length=50, null=True, blank=True, choices = CITY)

    def __str__(self):
        return self.company_name

