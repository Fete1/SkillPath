# promotions/forms.py
from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(label="Coupon Code")