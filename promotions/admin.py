# promotions/admin.py
from django.contrib import admin
from .models import Coupon,Wallet

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    search_fields = ['user__username']