from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # 'buyer' or 'seller'
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('users:register')
        user = CustomUser.objects.create_user(email=email, username=username, password=password, user_type=user_type)
        login(request, user)
        if user.user_type == 'buyer':
            return redirect('users:buyer_profile')
        else:
            return redirect('users:seller_profile')
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'buyer':
                return redirect('users:buyer_profile')
            else:
                return redirect('users:seller_profile')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('users:login')

# Create your views here.
