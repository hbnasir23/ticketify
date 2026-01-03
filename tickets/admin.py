from django.contrib import admin
from .models import Ticket

# This class defines how the table looks in the Admin Panel
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('subject', 'user', 'status', 'priority', 'category', 'created_at')
    
    # Add Filters on the right side
    list_filter = ('status', 'priority', 'category')
    
    # Add a Search Bar at the top
    search_fields = ('subject', 'description', 'user__username')
    
    # Make the list ordered by date (newest first)
    ordering = ('-created_at',)