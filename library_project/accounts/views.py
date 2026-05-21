from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

from .models import UserProfile


def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        email = request.POST.get('email')

        password1 = request.POST.get('password1')

        password2 = request.POST.get('password2')

        # Password check

        if password1 != password2:

            messages.error(request,
                           "Passwords do not match")

            return redirect('/accounts/register/')

        # Username exists

        if User.objects.filter(username=username).exists():

            messages.error(request,
                           "Username already exists")

            return redirect('/accounts/register/')

        # Create user

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create profile

        UserProfile.objects.create(
            user=user,
            role='member'
        )

       

        # Auto login
        messages.success(request, "Registration Successful! Please login.")
        return redirect('/accounts/login/')

    return render(request,
                  'register.html')

# Login View
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/accounts/dashboard/')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')


# Logout View

def logout_view(request):

    logout(request)

    return redirect('/')


# Dashboard View

def dashboard(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(request,
                  'dashboard.html',
                  {'profile': profile})
