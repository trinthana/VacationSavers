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

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

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
        log_entries = LogEntry.objects.filter(object_repr=current_user.username ).order_by('-timestamp')[:10]
        

        return render(request, 'pages/user-profile.html', context={
            'parent': 'Users',
            'segment': 'Profile',
            'user': {
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'username': current_user.username,
            },
            'auditlogs': log_entries
        })

    #if request.method == 'POST':

    #    form = EditProfileForm(request.POST, instance=CustomUser.objects.get(username=kwargs.get('username', request.user.username)))

        # Validate form
    #    if form.is_valid():

    #        user  = form.save()
    #        image = request.FILES.get('avatar-input', None)

    #        if cfg_FTP_UPLOAD() and image:

    #            try:
    #                avatar_url = helpers.upload(user.username, image)
    #                user.image = os.getenv("upload_url") + '/'.join(avatar_url.split("/")[-2:])
    #                user.save()
    #            except Exception as e:
    #                print(str(e))
    #                print("There is a problem in connection with FTP")
    #                return JsonResponse({
    #                    'errors': 'There is a problem in connection with FTP'
    #                }, status=400)

            # All good        
    #        return JsonResponse({}, status=200)

        # We have validation errors,
    #    return JsonResponse({'errors': str( form.errors )}, status=400)

@login_required(login_url="/accounts/login/")
def change_password2(request):
    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session to prevent reauthentication
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)

    current_user = request.user
    log_entries = LogEntry.objects.filter(object_repr=current_user.username ).order_by('-timestamp')[:10]
    return render(request, 'pages/user-profile.html', context={
        'parent': 'Users',
        'segment': 'Profile',
        'user': {
            'fullname': current_user.first_name + " " + current_user.last_name,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'username': current_user.username,
        },
        'auditlogs': log_entries,
        'form': form
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
