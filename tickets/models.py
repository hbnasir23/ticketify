from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Ticket(models.Model):
    # Dropdown Options
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Billing', 'Billing'),
        ('General', 'General'),
    ]

    # Database Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    # Logic to check if ticket is overdue (For Demo: > 10 Minutes)
    @property
    def is_overdue(self):
        # 1. Ticket must be 'Open'
        if self.status != 'Open':
            return False
        
        # 2. Check if it was created more than 10 minutes ago
        now = timezone.now()
        diff = now - self.created_at
        
        # timedelta(minutes=10) checks for 10 minutes
        # Change to timedelta(hours=24) if you want the real-world 24h rule later
        return diff > timedelta(minutes=10)