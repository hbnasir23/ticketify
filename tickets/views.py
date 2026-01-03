from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
# (Keep your existing imports)
from django.db.models import Q # <--- ADD THIS for search logic

@login_required
def dashboard(request):
    # 1. Base Query: Get current user's tickets
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')

    # 2. Search Logic (Search by Description or Subject)
    query = request.GET.get('q')
    if query:
        tickets = tickets.filter(
            Q(description__icontains=query) | Q(subject__icontains=query)
        )

    # 3. Filter Logic (Priority, Status, Category)
    priority_filter = request.GET.get('priority')
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')

    if priority_filter: tickets = tickets.filter(priority=priority_filter)
    if status_filter: tickets = tickets.filter(status=status_filter)
    if category_filter: tickets = tickets.filter(category=category_filter)

    # 4. Context Data for Stats
    # Note: We calculate stats based on ALL tickets, not just the filtered search result
    all_tickets = Ticket.objects.filter(user=request.user)
    
    context = {
        'tickets': tickets,
        # Status Counts
        'total_open': all_tickets.filter(status='Open').count(),
        'total_progress': all_tickets.filter(status='In Progress').count(),
        'total_resolved': all_tickets.filter(status='Resolved').count(),
        # Priority Counts
        'total_high': all_tickets.filter(priority='High').count(),
        'total_medium': all_tickets.filter(priority='Medium').count(),
        'total_low': all_tickets.filter(priority='Low').count(),
    }
    return render(request, 'tickets/dashboard.html', context)
    
# ADD A DELETE VIEW
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
    return redirect('dashboard')

# --- 1. SPLASH SCREEN (Root URL) ---
def splash(request):
    # If user is already logged in, send them to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'splash.html')

# --- 2. AUTHENTICATION (Signup) ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately
            login(request, user)
            messages.success(request, "Account created! Welcome to Ticketify.")
            return redirect('dashboard')
        else:
            # If there is an error (e.g., password too short), show it
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

# --- 3. DASHBOARD (View Tickets) ---
@login_required
def dashboard(request):
    # Get only the logged-in user's tickets
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tickets': tickets,
        'total_open': tickets.filter(status='Open').count(),
        'total_progress': tickets.filter(status='In Progress').count(),
        'total_resolved': tickets.filter(status='Resolved').count(),
    }
    return render(request, 'tickets/dashboard.html', context)

# --- 4. CREATE TICKET ---
@login_required
def create_ticket(request):
    if request.method == 'POST':
        Ticket.objects.create(
            user=request.user,
            subject=request.POST.get('subject'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
            category=request.POST.get('category', 'General') # Default to General if missing
        )
        messages.success(request, "Ticket created successfully!")
        return redirect('dashboard')
    return render(request, 'tickets/create_ticket.html')

# --- 5. UPDATE TICKET STATUS ---
@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.status = request.POST.get('status')
        ticket.save()
        messages.info(request, "Ticket updated.")
    return redirect('dashboard')