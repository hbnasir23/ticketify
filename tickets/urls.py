from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash, name='splash'),  # Root URL is now Splash
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
]