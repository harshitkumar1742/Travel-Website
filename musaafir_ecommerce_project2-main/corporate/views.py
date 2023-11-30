from django.shortcuts import render, redirect 
from .models import *
from home.models import Customer
from django.db.models import Q
from django.contrib import messages
from .forms import AddEmployeesForm, ContactUsForm, CompanySignUpForm, create_user_form
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout 
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from email.message import EmailMessage
from django.template.loader import render_to_string
from django.template import loader
from django.utils.html import strip_tags
import razorpay 



# Create your views here.

def corporate(request):
    try:
        name = request.user.customer
    except:
        name = "AnonymousUser"
    context={'name': name}
    return render(request, 'musaafir/corporate.html', context)


def contact_us_form(request):
    form = ContactUsForm(request.POST)
    if form.is_valid():
                data = ContactUs()
                data.name = form.cleaned_data['name']
                data.email = form.cleaned_data['email']
                data.company_name = form.cleaned_data['company_name']
                data.phone_number = form.cleaned_data['phone_number']
                data.comments = form.cleaned_data['comments']
                data.city = form.cleaned_data['city']
                data.save() 
                return redirect('corporate')

def company_signup_form(request):

    form = CompanySignUpForm(request.POST)
    if form.is_valid():
                data = CompanySignUp()
                data.name = form.cleaned_data['name']
                data.company_name = form.cleaned_data['company_name']
                data.phone_number = form.cleaned_data['phone_number']
                data.city = form.cleaned_data['city']
                data.save() 
                #User.objects.create(username=data.name, email=data.email)
                #Customer.objects.create(user=user,name=data.name,email=data.email, company_name=data.company_name)
                return redirect('company_signup_form2')

def company_signup_form2(request):

    form = create_user_form()
    if request.method == 'POST':
        form = create_user_form(request.POST)
        if form.is_valid():
            form.save()
            print(form.save)
            username=request.POST.get('username')
            password= request.POST.get('password')
            email=request.POST.get('email')
            user = form.save()
            company_name= CompanySignUp.objects.get(name=username)
            #so that user has a customer and no error is returned  
            Customer.objects.create(user=user,name=username,email=email,company_name=company_name)

            messages.success(request, 'Your CORPORATE account was successfully created! You can log in now')
            return redirect('login')
         
    context={'form': form}
    return render(request, 'musaafir/corporate_signup.html', context)  



def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
                login(request, user)
                if user.customer.company_name is not None:
                    return redirect('dashboard')
                else:
                    return redirect('home')
        else:
            login(request, user)
            return redirect('home')
    


    context={}
    return render(request, 'musaafir/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    customer = request.user.customer 
   

    context={'customer': customer}
    return render(request, 'musaafir/dashboard.html', context)
# will have to have an account before signing up 


def add_employees(request):
 
    customer = request.user.customer 
    company_name = customer.company_name
    employees = Customer.objects.filter(company_name=company_name)

    context={'company': company_name, 'employees': employees}
    return render(request, 'musaafir/add_employees.html', context)

def add_employees_form(request):
    form = AddEmployeesForm(request.POST)
    if form.is_valid():
                data = AddEmployees()
                data.name = form.cleaned_data['name']
                data.email = form.cleaned_data['email']
                data.company_name = request.user.customer.company_name
                data.budget = form.cleaned_data['budget']
                if request.user.customer.total_budget is None:
                  request.user.customer.total_budget = 0  
                if data.budget > request.user.customer.total_budget:
                    budget = data.budget
                    return redirect('corporate_payments', budget)
                else:
                    data.save()
                    total_budget = request.user.customer.total_budget - data.budget
                    AddEmployees.objects.filter(company_name=data.company_name).update(total_budget=total_budget)
                    Customer.objects.filter(company_name=data.company_name).update(total_budget=total_budget)


                    html_content = render_to_string("musaafir/emailbody.html", {'data': data})
                    text_content=strip_tags(html_content)
                    email = EmailMultiAlternatives('Welcome to Corporate Musaafir!', text_content, settings.EMAIL_HOST_USER, [data.email])
                    email.attach_alternative(html_content, "text/html")
                    email.send()

 
                    user = User.objects.create(username=data.name, email=data.email)
                    Customer.objects.create(user=user, name=data.name,email=data.email, company_name = data.company_name, budget=data.budget)    
                    return redirect('add_employees')

def corporate_payments(request, budget):
    company_name = request.user.customer.company_name
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    payment_order = client.order.create(dict(amount=budget*100, currency='INR', payment_capture = 1))
    payment_order_id = payment_order['id']
    AddEmployees.objects.filter(company_name=company_name, name=request.user.customer).update(total_budget=budget)
    Customer.objects.filter(company_name=company_name, name=request.user.customer).update(total_budget=budget)


    return render(request, 'musaafir/corporate_payments.html', {'api_key': settings.RAZORPAY_KEY_ID, 'order_id': payment_order_id, 'amount': budget})

def corporate_payment_success(request, budget):
    company_name = request.user.customer.company_name
    AddEmployees.objects.filter(company_name=company_name, name=request.user.customer).update(total_budget=budget)
    #Customer.objects.filter(company_name=company_name, name=request.user.customer).update(total_budget=budget)

    return redirect('add_employees')



