from django.contrib import admin
from .models import Affiliate

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('user', 'affiliate_code', 'is_active')
    raw_id_fields = ('user',)