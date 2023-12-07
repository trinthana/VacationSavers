from django import template
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from auditlog.models import LogEntry
from . import helpers
from app.forms import *
from app.models import *

# Create your views here.
#@login_required(login_url="/accounts/login/")
def index(request):

    # Page from the theme 
    if request.user.is_authenticated:
        return render(request, 'pages/index.html')
    else:
        return render(request, 'pages/landing.html')

@login_required(login_url="/accounts/login/")
def tourradar(request):
    context = {
    'parent': 'Tours',
    'segment': 'TourRadar'
    }

    # Page from the theme 
    return render(request, 'pages/tour-radar.html', context)

@login_required(login_url="/accounts/login/")
def smartfares(request):
    context = {
    'parent': 'Flights',
    'segment': 'Smartfares'
    }

    # Page from the theme 
    return render(request, 'pages/flight-smartfares.html', context)

@login_required(login_url="/accounts/login/")
def profile(request, **kwargs):

    if request.method == 'GET':
        current_user = request.user
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user)

        log_entries = LogEntry.objects.filter(object_repr=current_user.username ).order_by('-timestamp')[:10]
        

        return render(request, 'pages/user-profile.html', context={
            'parent': 'Users',
            'segment': 'Profile',
            'user': {
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'phone': user_profile.phone,
                'image': user_profile.image,
                'subscribed_package': user_profile.subscribed_package,
                'subscribed_date': user_profile.subscribed_date,
                'expired_date': user_profile.expired_date,
            },
            'auditlogs': log_entries
        })

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        profile_form = UserProfileForm(request.POST, instance=user_profile)

        # Validate form
        if profile_form.is_valid():

            profile_form.save()
            
            return redirect('user_profile')
            # All good        

        else:
            current_user = request.user
            try:
                user_profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile(user=request.user)

        log_entries = LogEntry.objects.filter(object_repr=current_user.username ).order_by('-timestamp')[:10]
        # We have validation errors,
        return render(request, 'pages/user-profile.html', context={
            'parent': 'Users',
            'segment': 'Profile',
            'user': {
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'phone': user_profile.phone,
                'image': user_profile.image,
                'subscribed_package': user_profile.subscribed_package,
                'subscribed_date': user_profile.subscribed_date,
                'expired_date': user_profile.expired_date,
            },
            'auditlogs': log_entries
        })


def change_password(request, **kwargs):

    form = SetPasswordForm(user=request.user, data=request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        message = 'Password successfully changed.'
        status = 200
        return redirect('password_change_done')
    else:
        message = form.errors
        status = 400
        return redirect('change_password')
    return JsonResponse({
        'message': message
    }, status=status)


def delete_account(request, **kwargs):
    result, message = helpers.delete_user(request.user)
    if not result:
        return JsonResponse({
            'errors': message
        }, status=400)
    logout(request)
    return HttpResponseRedirect('/login/')
