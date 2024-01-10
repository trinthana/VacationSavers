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
from rest_framework_multitoken.models import MultiToken

# Create your views here.
#@login_required(login_url="/accounts/login/")
def index(request):
    context = {
    'parent': 'Navigation',
    'segment': 'Dashboard'
    }

    # Page from the theme 
    if request.user.is_authenticated:
        return render(request, 'pages/index.html', context)
    else:
        return render(request, 'pages/landing.html')

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
            'parent': 'Account',
            'segment': 'Profile',
            'user': {
                'username': current_user.username,
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'phone': user_profile.phone,
                'image_file': user_profile.image_file,
                'subscribed_package': user_profile.subscribed_package,
                'subscribed_date': str(user_profile.subscribed_date or ''),
                'expired_date': str(user_profile.expired_date or ''),
            },
            'auditlogs': log_entries
        })

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        # Validate form
        if profile_form.is_valid():
            if 'image_file' in request.FILES:
                profile_form.image_file = request.FILES['image_file']
                print('Image = ', request.FILES['image_file'])
            profile_form.save()
            
            return redirect('user_profile')
            # All good        

        else:
            print(profile_form.errors)
            current_user = request.user
            try:
                user_profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile(user=request.user)

        log_entries = LogEntry.objects.filter(object_repr=current_user.username ).order_by('-timestamp')[:10]
        # We have validation errors,
        return render(request, 'pages/user-profile.html', context={
            'parent': 'Account',
            'segment': 'Profile',
            'user': {
                'username': current_user.username,
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': user_profile.address,
                'postal_code': user_profile.postal_code,
                'phone': user_profile.phone,
                'image_file': user_profile.image_file,
                'subscribed_package': user_profile.subscribed_package,
                'subscribed_date': str(user_profile.subscribed_date or ''),
                'expired_date': str(user_profile.expired_date or ''),
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
    return HttpResponseRedirect('/accounts/login/')

def verify_code(request, **kwargs):
    token_used = False
    try:
        if request.method == 'GET':
            inp_token = request.GET['token']
        elif request.method == 'POST':
            inp_token = request.POST['token']
    except:
        inp_token = ''

    if inp_token is not None and inp_token != '' : 
        try:
            token_count = MultiToken.objects.filter(key=inp_token).count()
            if token_count > 0 :
                try:
                    user_profile_count = UserProfile.objects.filter(token=inp_token).count()
                    if user_profile_count > 0 :
                        token_used = True
                    else :
                        token_used = False
                except UserProfile.DoesNotExist:
                    token_used = False
            
            else:
                return render(request, 'pages/signup-withcode.html', context={'message':'This invitation code is not valid.', 'token':inp_token})        

        except MultiToken.DoesNotExist:
            return render(request, 'pages/signup-withcode.html', context={'message':'This invitation code is not valid.', 'token':inp_token})        
    else :
        return render(request, 'pages/signup-withcode.html')

    if not token_used :
        request.session['token'] = inp_token
        url = reverse('register_withcode')
        return HttpResponseRedirect(url)

    else :
        return render(request, 'pages/signup-withcode.html', context={'message':'This invitation code is already used.', 'token':inp_token})        
    

@login_required(login_url="/accounts/login/")
def change_plan(request):
    context = {
    'parent': 'Account',
    'segment': 'Change Plan'
    }

    # Page from the theme 
    return render(request, 'pages/change-plan.html', context)

@login_required(login_url="/accounts/login/")
def timefortickets(request):
    context = {
    'parent': 'Tickets',
    'segment': 'Time for Tickets'
    }

    # Page from the theme 
    return render(request, 'pages/ticket-timefortickets.html', context)

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
def access_travel(request):
    # Query the ApplicationToken model to get the token for application 'ACCESS' and the current user
    try:
        application_token = ApplicationToken.objects.get(user=request.user, application=ApplicationChoices.ACCESS)
        cvt = application_token.token
    except ApplicationToken.DoesNotExist:
        # Handle the case where no token is found for the specified application and user
        cvt = None

    context = {
    'parent': 'All-in-1',
    'segment': 'Access Travel',
    'cvt': cvt
    }

    # Page from the theme 
    return render(request, 'pages/access-travel.html', context)

@login_required(login_url="/accounts/login/")
def access_deals(request):
    # Query the ApplicationToken model to get the token for application 'ACCESSDEAL' and the current user
    try:
        application_token = ApplicationToken.objects.get(user=request.user, application=ApplicationChoices.ACCESSDEAL)
        cvt = application_token.token
    except ApplicationToken.DoesNotExist:
        # Handle the case where no token is found for the specified application and user
        cvt = None

    context = {
    'parent': 'All-in-1',
    'segment': 'Access Deals',
    'cvt': cvt
    }

    # Page from the theme 
    return render(request, 'pages/access-deals.html', context)