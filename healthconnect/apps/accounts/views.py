from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomRegistrationForm
from .models import CustomUser, StaffProfile
from apps.patients.models import PatientProfile
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegistrationForm()

    return render(request, 'register.html', {'form': form})

def forgot_password_view(request):
    # Logic for forgot password
    return render(request, 'forgot-password.html')


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
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    user_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birthdate': user.birthdate,
    }

    if user.role == 'patient':
        try:
            patient_profile = PatientProfile.objects.get(user=user)
            user_info['medical_history'] = patient_profile.medical_history
        except PatientProfile.DoesNotExist:
            user_info['medical_history'] = 'No medical history available.'

    else:
        try:
            staff_profile = StaffProfile.objects.get(user=user)
            user_info['role'] = staff_profile.role
        except StaffProfile.DoesNotExist:
            user_info['role'] = 'No role available.'

    return render(request, 'profile.html', {'user_info': user_info})


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

def services(request):
    return render(request, 'services.html')

def pharmacy(request):
    return render(request, 'pharmacy.html')