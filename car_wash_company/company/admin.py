from django.contrib import admin
from .models import Order, Branch, Washer, CarType

admin.site.register([Order, Branch, Washer, CarType])