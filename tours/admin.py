# tours/admin.py
from django.contrib import admin
from .models import Destination, City, Tour

admin.site.register(Destination)
admin.site.register(City)
admin.site.register(Tour)