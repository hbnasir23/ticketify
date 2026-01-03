from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash, name='splash'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'), # <--- New Page
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]