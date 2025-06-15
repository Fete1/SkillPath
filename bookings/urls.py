# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancelled/', views.payment_cancelled, name='payment_cancelled'),
]