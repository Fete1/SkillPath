# affiliates/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Affiliate

@login_required
def affiliate_dashboard(request):
    try:
        affiliate = request.user.affiliate
    except Affiliate.DoesNotExist:
        affiliate = None
    context = {'affiliate': affiliate}
    return render(request, 'affiliates/dashboard.html', context)