from django.contrib import admin
from .models import FAQ, SupportTicket, TicketMessage

admin.site.register(FAQ)

class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    readonly_fields = ('user', 'message', 'timestamp')
    extra = 0

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    inlines = [TicketMessageInline]