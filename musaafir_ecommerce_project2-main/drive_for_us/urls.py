from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('drive_for_us', views.drive_for_us, name="drive_for_us"),
    path('need_car/', views.need_car, name="need_car"),
    path('need_car_form/', views.need_car_form, name="need_car_form"),
    path('attach_car/', views.attach_car, name="attach_car"),
    path('attach_car_form/', views.attach_car_form, name="attach_car_form"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)