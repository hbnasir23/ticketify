from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This enables Django's built-in Login/Logout views automatically
    path('accounts/', include('django.contrib.auth.urls')),
    # This connects your 'tickets' app for the dashboard and signup
    path('', include('tickets.urls')),
]