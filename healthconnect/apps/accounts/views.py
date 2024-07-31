from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser, PatientProfile, StaffProfile

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user.is_patient:
                PatientProfile.objects.create(user=user)
            else:
                StaffProfile.objects.create(user=user, role=get_staff_role(user))
            auth_login(request, user)
            return redirect('profile')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            role = request.GET.get('role', '')
            if role == 'doctor':
                return redirect('doctor_dashboard')  # Replace with actual dashboard URL
            elif role == 'patient':
                return redirect('patient_dashboard')  # Replace with actual dashboard URL
            elif role == 'nurse':
                return redirect('nurse_dashboard')  # Replace with actual dashboard URL
            elif role == 'pharmacist':
                return redirect('pharmacist_dashboard')  # Replace with actual dashboard URL
            return redirect('profile')  # Default redirect if no role is specified
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def profile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_patient:
            profile = user.patientprofile
        else:
            profile = user.staffprofile
        return render(request, 'accounts/profile.html', {'profile': profile})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated

def get_staff_role(user):
    if user.is_doctor:
        return 'Doctor'
    elif user.is_nurse:
        return 'Nurse'
    elif user.is_pharmacist:
        return 'Pharmacist'
    return ''

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')