# bookings/admin.py
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'booking_date', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'tour')