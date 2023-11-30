from django.shortcuts import render, redirect 
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CityCabReviewsForm, create_user_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from geopy.geocoders import Nominatim 
from geopy.distance import geodesic 
from corporate.models import AddEmployees
from django.conf import settings
import razorpay 
from django.views.decorators.csrf import csrf_exempt




def signup(request):
    form = create_user_form()
    if request.method == 'POST':
        form = create_user_form(request.POST)
        if form.is_valid():
            form.save()
            print(form.save)
            username=request.POST.get('username')
            password1= request.POST.get('password1')
            password2=request.POST.get('password2')
            email=request.POST.get('email')
            user = form.save()
            #so that user has a customer and no error is returned  
            Customer.objects.create(user=user,name=username,email=email)

            messages.success(request, 'Your account was successfully created! You can log in now')
            return redirect('login')
            

    context={'form': form}
    return render(request, 'musaafir/signup.html', context)

def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
       

        if user is not None:
            if request.user.customer.company_name is None:
                login(request, user)
                return redirect('dashboard')
            else:
                login(request, user)
                return redirect('home')

    context={}
    return render(request, 'musaafir/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('home')


def home(request):
    
    context={}
    return render(request, 'musaafir/home.html', context)


def citycab(request):
    cabs = CityCab.objects.all()
    if request.method == 'GET':
        pickup_city = request.GET.get('city')
        datetime=request.GET.get('datetime')
        destination=request.GET.get('destination')
        passengers = request.GET.get('passengers')
        hourly_package = request.GET.get('hourly_package')
        car_option = request.GET.get('car_option')



        if passengers is not None and pickup_city is not None:
            cabs = cabs.filter(Q(pickup_city__icontains=pickup_city) & Q(no_of_passengers__icontains=passengers) & Q(car_option__icontains=car_option))

        elif passengers is not None and pickup_city is not None and hourly_package is not None:
            cabs = cabs.filter(Q(pickup_city__icontains=pickup_city) & Q(hourly_package__icontains=hourly_package) & Q(no_of_passengers__icontains=passengers)  & Q(car_option__icontains=car_option))


    context={'cabs': cabs }
    return render(request, 'musaafir/citycab.html', context)

def citycab_booking(request, name, id):
    cabs  = CityCab.objects.get(name=name)
    cab = CityCab.objects.get(name=name, id=id)
    user= request.user.customer

    if request.method == 'GET':
        pickup=request.GET.get('pickup')
        datetime=request.GET.get('datetime')
        print("++++++++++++++++++++", cab.car_option)
        if cab.car_option != 'RENTAL':
            destination=request.GET.get('destination')
        else:
            hourly_package=request.GET.get('hourly_package')

    if cab.car_option != 'RENTAL':
        geocoder = Nominatim(user_agent='location')
        location1= pickup 
        location2= destination
        coordinates1= geocoder.geocode(location1)
        coordinates2= geocoder.geocode(location2)
        lat1, long1 = (coordinates1.latitude), (coordinates1.longitude) 
        lat2, long2 = (coordinates2.latitude), (coordinates2.longitude) 
        place1= (lat1, long1)
        place2= (lat2, long2)
        distance = geodesic(place1, place2).km
        price_per_km = cabs.price
        price = int(price_per_km * distance)
        CityCabBooking(customer = user, price=price, pickup=pickup, destination=destination, pickup_datetime=datetime, cabname=cabs, payment_done=False).save()
    else:
        price_per_km = int(cabs.price)
        price = int(price_per_km * int(hourly_package))
        CityCabBooking(customer = user, price=price, pickup=pickup, destination='RENTAL', pickup_datetime=datetime, cabname=cabs, payment_done=False).save()




    return redirect('checkout', id, price)

def cab_view(request, name, id, car_option):
    cabs  = CityCab.objects.get(name=name)
    cab  = CityCab.objects.get(name=name, id=id, car_option=car_option)
        
    reviews = CityCab_Reviews.objects.filter(name=id)

    context={'product': cabs, 'cab': cab, 'reviews' : reviews, 'car_option': car_option }
    return render(request, 'musaafir/cab_view.html', context)

def city_cab_review(request, name, id, car_option):
    try:
            reviews = CityCab_Reviews.objects.get(customer=request.user.customer, name_id=id)
            form = CityCabReviewsForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('cab_view', name=name, id=id, car_option=car_option)        
            
    except CityCab_Reviews.DoesNotExist:
            form = CityCabReviewsForm(request.POST)
            if form.is_valid():
                data = CityCab_Reviews()
                data.subject = form.cleaned_data['subject']
                data.rate = form.cleaned_data['rate']
                data.review = form.cleaned_data['review']
                data.customer = request.user.customer
                data.name_id = id
                data.save() 
                messages.success(request, 'Thank you, your review has been submitted!')
                return redirect('cab_view', name=name, id=id, car_option=car_option)


def checkout(request, id, price):

    cab = CityCabBooking(id=id, price=price)
    budget = request.user.customer.budget 
    #updated_budget = budget 
    if cab.price > budget:
        total = cab.price - budget
        budget= 0
        total1 = total * 100 
        Customer.objects.filter(name=request.user.customer).update(budget=budget)
        AddEmployees.objects.filter(name=request.user.customer).update(budget=budget)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        payment_order = client.order.create(dict(amount=total1, currency='INR', payment_capture = 1))
        callback_url = "http://127.0.0.1:8000/payment_success/" + str(price) +str(id)
        print(callback_url)
        payment_order_id = payment_order['id']
        
        context={'cab': cab, 'price': price, 'id': id, 'budget': budget, 'total': total, 'api_key': settings.RAZORPAY_KEY_ID, 'order_id': payment_order_id, 'callback_url': callback_url}
        return render(request, 'musaafir/checkout.html', context)
    
        
    elif cab.price < budget:
        total = 0
        budget = budget - cab.price
        Customer.objects.filter(name=request.user.customer).update(budget=budget)
        AddEmployees.objects.filter(name=request.user.customer).update(budget=budget)


        return redirect('payment_success', id=id)


    elif cab.price == budget:
        total = 0
        budget=0
        Customer.objects.filter(name=request.user.customer).update(budget=budget)
        AddEmployees.objects.filter(name=request.user.customer).update(budget=budget)
        return redirect('payment_success', price=price)

    return redirect('payment_success', id=id)


def payment_success(request, id):
    CityCabBooking.objects.filter(customer = request.user.customer, cabname_id=id).update(payment_done=True)

    return redirect('home')


def cancel(request, id, pickup_datetime):
    CityCabBooking.objects.filter(customer = request.user.customer, cabname_id=id, payment_done=True, can_cancel=True, pickup_datetime=pickup_datetime).delete()

    return redirect('profile_page')


def profile_page(request):
    customer = request.user.customer
    name = customer.name 
    cab_bookings= CityCabBooking.objects.filter(customer=customer, payment_done=True)
 

    return render(request, 'musaafir/profile_page.html', {'name': name, 'cab_bookings': cab_bookings})








