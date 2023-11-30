from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings 
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('corporate', views.corporate, name="corporate"),
    path('contact_us_form', views.contact_us_form, name="contact_us_form"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('add_employees_form', views.add_employees_form, name="add_employees_form"),    
    path('add_employees/', views.add_employees, name="add_employees"),
    path('company_signup_form', views.company_signup_form, name="company_signup_form"),
    path('company_signup_form2', views.company_signup_form2, name="company_signup_form2"),
    path('corporate_payments/<int:budget>', views.corporate_payments, name="corporate_payments"),
    path('corporate_login/', views.loginpage, name='login'),
    path('corporate_logout/', views.logoutpage, name='logout'),
    path('create_password/', auth_views.PasswordResetView.as_view(template_name= "musaafir/password_setting_corporate.html"), name="create_password"),
    path('create_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name= "musaafir/email_sent.html"), name="password_reset_done"),
    path('set/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= "musaafir/new_password.html"), name ="password_reset_confirm"),
    path('create_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name= "musaafir/password_set.html"), name="password_reset_complete"),
    path('corporate_payments/<int:budget>/corporate_payment_success', views.corporate_payment_success, name="corporate_payment_success")



    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)