from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import CityCab_Reviews

class CityCabReviewsForm(forms.ModelForm):
    class Meta:
        model = CityCab_Reviews
        fields= ['subject', 'review', 'rate' ]

class create_user_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        