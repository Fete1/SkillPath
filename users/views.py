from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from .forms import MinimalistUserCreationForm
# users/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from affiliates.models import Affiliate
from promotions.models import Wallet

class SignUpView(generic.CreateView):
    # Use our new, clean form
    form_class = MinimalistUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    # Override the form_valid method
    def form_valid(self, form):
        # Save the new user object
        response = super().form_valid(form)
        # Check the session for a referral code
        ref_code = self.request.session.get('affiliate_ref')
        if ref_code:
            try:
                affiliate = Affiliate.objects.get(affiliate_code=ref_code)
                # self.object is the newly created user
                # Link the user's profile to the affiliate
                self.object.profile.referred_by = affiliate
                self.object.profile.save()
            except Affiliate.DoesNotExist:
                # The code is invalid, do nothing
                pass
        return response
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Get the user's wallet, or None if it somehow doesn't exist
    wallet = Wallet.objects.filter(user=request.user).first()

    context = {
        'bookings': bookings,
        'wallet': wallet, # Add the wallet to the context
    }
    return render(request, 'users/dashboard.html', context)