from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(CityCab)
admin.site.register(CityCab_Reviews)
admin.site.register(CityCabBooking)

