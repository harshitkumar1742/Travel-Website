from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('checkout/<int:id>/<int:price>', views.checkout, name='checkout'),
    path('checkout/<int:id>/payment_success', views.payment_success, name="payment_success"),
    path('city_commute', views.citycab, name="citycab"),
    path('citycab_booking/<str:name>/<int:id>', views.citycab_booking, name="citycab_booking"),
    path('cab_view/<str:name>/<int:id>/<str:car_option>', views.cab_view, name="cab_view"),
    path('city_cab_review/<str:name>/<int:id>/<str:car_option>', views.city_cab_review, name="city_cab_review"),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('cancel/<int:id>/<str:pickup_datetime>', views.cancel, name="cancel"),






]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)