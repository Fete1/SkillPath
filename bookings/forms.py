# bookings/forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    # Add widgets to apply Bootstrap classes
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'})
    )
    number_of_guests = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'min': 1}),
        label="Number of Guests"
    )

    class Meta:
        model = Booking
        fields = ['booking_date', 'number_of_guests']