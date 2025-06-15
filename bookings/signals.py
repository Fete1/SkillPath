# bookings/signals.py
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Booking

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        booking = get_object_or_404(Booking, id=ipn.invoice)

        if booking.total_price == ipn.mc_gross:
            # Mark the order as paid
            booking.status = 'CONFIRMED'
            booking.save()