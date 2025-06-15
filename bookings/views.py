# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm

from .models import Booking
from promotions.models import Coupon, Wallet
from promotions.forms import CouponApplyForm

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    coupon_apply_form = CouponApplyForm(request.POST or None)
    discount = 0

    if coupon_apply_form.is_valid():
        code = coupon_apply_form.cleaned_data['code']
        now = timezone.now()
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                is_active=True
            )
            discount = coupon.discount
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            # You can optionally add a message here

    # Recalculate total with discount
    final_price = booking.total_price
    if discount > 0:
        final_price = final_price - (final_price * (discount / 100))

    # NEW: Apply wallet balance
    wallet_deduction = 0
    try:
        wallet = request.user.wallet
        if wallet.balance > 0:
            if wallet.balance >= final_price:
                wallet_deduction = final_price
            else:
                wallet_deduction = wallet.balance
            final_price -= wallet_deduction
    except Wallet.DoesNotExist:
        wallet = None  # Shouldn't happen if wallet is auto-created via signal

    # Prepare PayPal form only if needed
    if final_price <= 0:
        form = None  # No PayPal payment needed
    else:
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': f"{final_price:.2f}",
            'item_name': f"Booking for {booking.tour.name}",
            'invoice': str(booking.id),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment_success')}",
            'cancel_return': f"http://{host}{reverse('payment_cancelled')}",
        }
        form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'booking': booking,
        'form': form,
        'coupon_apply_form': coupon_apply_form,
        'discount': discount,
        'wallet_deduction': wallet_deduction,
        'final_price': final_price + wallet_deduction,  # Original total before wallet
        'price_to_pay': final_price,  # What the user still owes
        'wallet_covers_all': final_price <= 0,
    }
    return render(request, 'bookings/process_payment.html', context)

def payment_success(request):
    return render(request, 'bookings/payment_success.html')

def payment_cancelled(request):
    return render(request, 'bookings/payment_cancelled.html')
