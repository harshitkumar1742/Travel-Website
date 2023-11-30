from django import forms 
from .models import ContactUs, CompanySignUp, AddEmployees
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields= ['name', 'email', 'phone_number', 'company_name', 'city', 'comments']

class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = CompanySignUp
        fields= ['name','phone_number', 'company_name', 'city']


class AddEmployeesForm(forms.ModelForm):
    class Meta:
        model = AddEmployees
        fields= ['name', 'email', 'company_name', 'budget', 'total_budget']


class create_user_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']