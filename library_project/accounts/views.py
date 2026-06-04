from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import UserProfile

from books.models import (
    IssuedBook,
    Reservation
)


# REGISTER
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect('/accounts/register/')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect('/accounts/register/')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        UserProfile.objects.create(
            user=user,
            role='member'
        )

        messages.success(
            request,
            "Registration Successful! Please login."
        )

        return redirect('/accounts/login/')

    return render(
        request,
        'register.html'
    )


# LOGIN
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        'login.html'
    )


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect('/')


# DASHBOARD
@login_required
def dashboard(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'dashboard.html',
        {
            'profile': profile
        }
    )


# PROFILE PAGE
@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    issued_count = IssuedBook.objects.filter(
        user=request.user
    ).count()

    reserved_count = Reservation.objects.filter(
        user=request.user
    ).count()

    pending_fine = IssuedBook.objects.filter(
        user=request.user,
        status='Issued'
    ).aggregate(
        total=Sum('fine')
    )['total'] or 0

    return render(
        request,
        'profile.html',
        {
            'profile': profile,
            'issued_count': issued_count,
            'reserved_count': reserved_count,
            'pending_fine': pending_fine,
        }
    )