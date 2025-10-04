from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, ClientForm, MedicalEditForm
from .models import CustomUser, Client
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

def is_doctor(user):
    return user.is_authenticated and (user.user_type == 'doctor' or user.is_superuser)

def is_receptionist(user):
    return user.is_authenticated and user.user_type == 'receptionist'

@login_required
def client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    return render(request, 'core/client.html', {
        'client': client,
        'user_type': request.user.user_type
    })

    
    # Check if user has permission to view this client
    if request.user.user_type == 'receptionist' and client.created_by != request.user:
        return redirect('dashboard_view')
    
    return render(request, 'core/client.html', {
        'client': client,
        'user_type': request.user.user_type
    })


@login_required
@user_passes_test(is_doctor, login_url='/dashboard/')
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('dashboard_view')
    return redirect('edit_client_medical', client_id=client_id)

@login_required
@user_passes_test(is_doctor, login_url='/dashboard/')
def edit_client_medical(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = MedicalEditForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('dashboard_view')
    else:
        form = MedicalEditForm(instance=client)  # This pre-fills all fields!
    
    return render(request, 'core/edit_medical.html', {
        'client': client,
        'form': form  # Pass the form to template
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            return redirect('dashboard_view')  # Make sure this matches your URL name
        else:
            # This will show form errors in the template
            print("Form errors:", form.errors)
    else:
        form = ClientForm()
    
    return render(request, 'add_client.html', {'form': form})


@login_required
def dashboard(request):
    user_type = request.user.user_type
    doctors = CustomUser.objects.filter(user_type='doctor')
    
    # All users see all clients
    clients = Client.objects.all().select_related('created_by', 'referred_to')
    
    # Calculate pending referrals for doctor
    if user_type == 'doctor':
        pending_referrals_count = clients.filter(
            referred_to=request.user, 
            referral_status='pending'
        ).count()
    
    # AJAX search request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_query = request.GET.get('q', '').strip()
        
        if search_query:
            clients = clients.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        clients_html = render_to_string('core/clients_table.html', {
            'clients': clients,
            'user_type': user_type
        })
        
        # Stats for doctor
        if user_type == 'doctor':
            stats = {
                'total_clients': clients.count(),
                'my_patients_count': clients.filter(
                    Q(referred_to=request.user) | 
                    Q(diagnosis__isnull=False)
                ).distinct().count(),
                'pending_referrals': pending_referrals_count,
                'completed_treatments': clients.filter(
                    treatment_plan__isnull=False,
                    diagnosis__isnull=False
                ).count(),
                'new_today': clients.filter(
                    created_at__date=timezone.now().date()
                ).count()
            }
        else:
            stats = {
                'total_clients': clients.count(),
                'with_diagnosis': clients.filter(diagnosis__isnull=False).count(),
                'today_count': clients.filter(created_at__date=timezone.now().date()).count(),
                'referred_count': clients.filter(is_referred=True).count()
            }
        
        return JsonResponse({
            'clients_html': clients_html,
            'total_count': clients.count(),
            'stats': stats
        })
    
    # Regular request
    total_clients = clients.count()
    
    if user_type == 'doctor':
        context = {
            'user_type': user_type,
            'doctors': doctors,
            'clients': clients,
            'total_clients': total_clients,
            'my_patients_count': clients.filter(
                Q(referred_to=request.user) | 
                Q(diagnosis__isnull=False)
            ).distinct().count(),
            'pending_referrals': pending_referrals_count,
            'completed_treatments': clients.filter(
                treatment_plan__isnull=False,
                diagnosis__isnull=False
            ).count(),
            'new_today': clients.filter(created_at__date=timezone.now().date()).count(),
        }
    else:
        context = {
            'user_type': user_type,
            'doctors': doctors,
            'clients': clients,
            'total_clients': total_clients,
            'diagnosed_count': clients.filter(diagnosis__isnull=False).count(),
            'today_count': clients.filter(created_at__date=timezone.now().date()).count(),
            'referred_count': clients.filter(is_referred=True).count(),
        }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def pending_referrals_view(request):
    if request.user.user_type != 'doctor':
        return redirect('dashboard')
    
    # Get all pending referrals
    pending_referrals = Client.objects.filter(
        referred_to=request.user, 
        referral_status='pending'
    ).select_related('created_by')
    
    context = {
        'user_type': 'doctor',
        'clients': pending_referrals,
        'title': 'Pending Referrals'
    }
    
    return render(request, 'core/pending_referrals.html', context)

@login_required
def check_notifications(request):
    if request.user.user_type != 'doctor':
        return JsonResponse({'pending_referrals': 0})
    
    pending_count = Client.objects.filter(
        referred_to=request.user, 
        referral_status='pending'
    ).count()
    
    return JsonResponse({'pending_referrals': pending_count})

@login_required
def refer_client(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            client_id = request.POST.get('client_id')
            referred_to_id = request.POST.get('referred_to')
            referral_notes = request.POST.get('referral_notes', '')
            
            client = Client.objects.get(id=client_id)
            referred_to = CustomUser.objects.get(id=referred_to_id, user_type='doctor')
            
            # Update referral info
            client.referred_to = referred_to
            client.referral_status = 'pending'
            client.referral_notes = referral_notes
            client.is_referred = True
            client.referred_at = timezone.now()
            client.referral_completed_at = None
            client.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'Client referred to Dr. {referred_to.username} successfully!'
            })
            
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doctor not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def mark_referral_seen(request, client_id):
    if request.method == 'POST' and request.user.user_type == 'doctor':
        try:
            client = Client.objects.get(id=client_id, referred_to=request.user)
            client.referral_seen_by_doctor = True
            client.save()
            return JsonResponse({'success': True})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})



@login_required
def complete_referral(request, client_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            client = Client.objects.get(id=client_id)
            
            if request.user.user_type == 'doctor':
                client.referral_status = 'completed'
                client.referral_completed_at = timezone.now()
                client.save()
                
                return JsonResponse({'success': True, 'message': 'Referral completed!'})
            else:
                return JsonResponse({'success': False, 'error': 'Only doctors can complete referrals'})
                
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Client not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})





@login_required
@user_passes_test(is_doctor, login_url='/dashboard/')
def signup_view(request):
    # If user is already authenticated, redirect to dashboard
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect to login after successful signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})

def home_view(request):
    return render(request, 'core/home.html',)

def about_view(request):
    return render(request, 'core/about.html',)

def service_view(request):
    return render(request, 'core/service.html',)

def contact_view(request):
    return render(request, 'core/contact.html',)
