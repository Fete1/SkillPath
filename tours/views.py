# tours/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tour
from bookings.forms import BookingForm
from bookings.models import Booking
from django.db.models import Sum

def tour_list(request):
    # ... (this view stays the same)
    tour_list = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tour_list': tour_list})

# The new and improved tour_detail view
def tour_detail(request, slug):
    tour = get_object_or_404(Tour, slug=slug)
    booking_form = BookingForm(request.POST or None)

    if request.method == 'POST':
        # This part only runs if the form is submitted
        if not request.user.is_authenticated:
            return redirect('login') # or show a message

        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Availability Check
            date = booking_form.cleaned_data['booking_date']
            guests = booking_form.cleaned_data['number_of_guests']

            # Calculate guests already booked for that date
            booked_guests = Booking.objects.filter(tour=tour, booking_date=date, status='CONFIRMED').aggregate(total_guests=Sum('number_of_guests'))['total_guests'] or 0

            if (booked_guests + guests) > tour.max_guests:
                messages.error(request, f"Sorry, not enough availability on {date}. Only {tour.max_guests - booked_guests} spots left.")
            else:
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.tour = tour
                booking.total_price = tour.price * booking.number_of_guests
                # The status is PENDING by default
                booking.save()
                # Redirect to a new "process_payment" view
                return redirect('process_payment', booking_id=booking.id)

    # This part runs for a normal GET request
    context = {
        'tour': tour,
        'booking_form': booking_form
    }
    return render(request, 'tours/tour_detail.html', context)