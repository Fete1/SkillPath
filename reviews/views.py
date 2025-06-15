# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from tours.models import Tour
from bookings.models import Booking
from .forms import ReviewForm

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    # SECURITY CHECK: User can only review a tour they have a CONFIRMED booking for.
    if not Booking.objects.filter(user=request.user, tour=tour, status='CONFIRMED').exists():
        messages.error(request, "You can only review tours you have booked.")
        return redirect('dashboard')

    # Check if the user has already reviewed this tour
    if Review.objects.filter(user=request.user, tour=tour).exists():
        messages.error(request, "You have already reviewed this tour.")
        return redirect('tour_detail', slug=tour.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted and is awaiting approval.")
            return redirect('tour_detail', slug=tour.slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'tour': tour
    }
    return render(request, 'reviews/add_review.html', context)