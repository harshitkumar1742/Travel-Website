from django import forms 
from .models import NeedCar, AttachCar

class NeedCarForm(forms.ModelForm):
    class Meta:
        model = NeedCar
        fields= ['name', 'phone_number', 'city' ]

class AttachCarForm(forms.ModelForm):
    class Meta:
        model = AttachCar
        fields= ['name', 'phone_number', 'city', 'car_type' ]

        