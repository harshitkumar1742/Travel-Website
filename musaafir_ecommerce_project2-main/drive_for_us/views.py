from django.shortcuts import render, redirect 
from .models import *
from django.db.models import Q
from .forms import NeedCarForm, AttachCarForm
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def drive_for_us(request):
    return render(request, 'musaafir/drive_for_us.html')


def need_car(request):
    return render(request, 'musaafir/need_car.html')


def need_car_form(request):
    form = NeedCarForm(request.POST)
    if form.is_valid():
                data = NeedCar()
                data.name = form.cleaned_data['name']
                data.phone_number = form.cleaned_data['phone_number']
                data.city = form.cleaned_data['city']
                data.save() 
                return redirect('need_car')

def attach_car(request):
    return render(request, 'musaafir/attach_car.html')


def attach_car_form(request):
    form = AttachCarForm(request.POST)
    if form.is_valid():
                data = AttachCar()
                data.name = form.cleaned_data['name']
                data.phone_number = form.cleaned_data['phone_number']
                data.city = form.cleaned_data['city']
                data.car_type = form.cleaned_data['car_type']
                data.save() 
                return redirect('attach_car')


