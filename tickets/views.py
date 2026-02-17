from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ticket


def splash(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'splash.html')

# --- 2. AUTHENTICATION ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Welcome.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- 3. PROFILE PAGE ---
@login_required
def profile(request):
    return render(request, 'tickets/profile.html')

# --- 4. DASHBOARD (MAIN LOGIC) ---
@login_required
def dashboard(request):
    # 1. Base Query
    tickets = Ticket.objects.filter(user=request.user)

    # 2. Search Logic
    query = request.GET.get('q')
    if query:
        tickets = tickets.filter(
            Q(description__icontains=query) | Q(subject__icontains=query)
        )

    # 3. Filter Logic
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if category_filter:
        tickets = tickets.filter(category=category_filter)

    # 4. Date Sorting Logic (New Feature)
    date_sort = request.GET.get('date_sort')
    if date_sort == 'oldest':
        tickets = tickets.order_by('created_at') 
    else:
        tickets = tickets.order_by('-created_at') 

    # 5. Stats Calculations
    all_tickets = Ticket.objects.filter(user=request.user)
    
    context = {
        'tickets': tickets,
        'total_open': all_tickets.filter(status='Open').count(),
        'total_progress': all_tickets.filter(status='In Progress').count(),
        'total_resolved': all_tickets.filter(status='Resolved').count(),
        'total_high': all_tickets.filter(priority='High').count(),
        'total_medium': all_tickets.filter(priority='Medium').count(),
        'total_low': all_tickets.filter(priority='Low').count(),
    }
    return render(request, 'tickets/dashboard.html', context)

# --- 5. CREATE TICKET ---
@login_required
def create_ticket(request):
    if request.method == 'POST':
        Ticket.objects.create(
            user=request.user,
            subject=request.POST.get('subject'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
            category=request.POST.get('category', 'General')
        )
        messages.success(request, "Ticket created successfully!")
        return redirect('dashboard')
    return render(request, 'tickets/create_ticket.html')

# --- 6. UPDATE TICKET  ---
@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.description = request.POST.get('description')
        ticket.category = request.POST.get('category')
        ticket.priority = request.POST.get('priority')
        ticket.status = request.POST.get('status')
        ticket.save()
        messages.success(request, "Ticket updated.")
    return redirect('dashboard')

# --- 7. DELETE TICKET ---
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket deleted.")
    return redirect('dashboard')