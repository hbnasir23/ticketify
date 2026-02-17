from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'priority', 'category', 'created_at')
    
    list_filter = ('status', 'priority', 'category')
    
    search_fields = ('subject', 'description', 'user__username')
    
    ordering = ('-created_at',)