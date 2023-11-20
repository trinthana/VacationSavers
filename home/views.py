from django.shortcuts import render
from django.http import HttpResponse

from django import template
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from auditlog.models import LogEntry


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
        log_entries = LogEntry.objects.filter(object_repr=current_user.username)
        

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

