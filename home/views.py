from django import template
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.db.models.functions import TruncMonth, ExtractYear, ExtractMonth
from django.db.models import Min, Max, Count, Sum
from django.core.exceptions import *

from auditlog.models import LogEntry
from app.forms import *
from app.models import *
from rest_framework_multitoken.models import MultiToken

from home import helpers
#---------------
# For Worldia, Arrivia
from home import arrivia
from home import accessdev
from requests.structures import CaseInsensitiveDict

from datetime import datetime, timedelta
from urllib.parse import urlencode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

import os
import base64
import requests, json, hashlib

#----------------
def openssl_encrypt(data, method, key, iv):
    # Ensure key and IV lengths match the expected sizes for AES-256-CBC
    if method == 'AES-256-CBC':
        key = key[:32]  # Use the first 32 bytes of the key for AES-256
        iv = iv[:16]  # Use the first 16 bytes of the IV for AES-256 in CBC mode
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()  # AES block size is 128 bits
        padded_data = padder.update(data.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted).decode()
    else:
        raise ValueError("Unsupported encryption method")

def openssl_random_pseudo_bytes(length, crypto_strong=True):
    """
    Generate cryptographically strong pseudo-random bytes.

    :param length: Number of random bytes to generate.
    :param crypto_strong: If True, ensures the random bytes are cryptographically strong.
    :return: A bytes object containing random bytes.
    """
    # In Python's os.urandom, the bytes are always cryptographically strong,
    # so the crypto_strong parameter does not change the behavior as it would in PHP.
    return os.urandom(length)

# End Worldia
#---------------

#---------------
# For General Purposes
def get_credential(user, app):
    if user and app:
        try:
            application_token = ApplicationToken.objects.get(user__username=user, application=app)
            return application_token.token, application_token.custom1, application_token.custom2, application_token.custom3
        except MultipleObjectsReturned:
            return application_token.token, application_token.custom1, application_token.custom2, application_token.custom3

        except ApplicationToken.DoesNotExist:
            return "", "", "", ""
        
def get_or_create_user_profile(username):
    # Get or create the UserProfile record based on the provided username
    user_profile, created = UserProfile.objects.get_or_create(user__username=username)

    # If the record is created, it means it was not found and a new record was created
    if created:
        user_profile.save()

    return user_profile

                
# End General Purposes
#---------------

##############################################################################################################################
#---------------
# Create your views here.
#@login_required(login_url="/accounts/login/")
def index(request):
    context = {
    'parent': 'Navigation',
    'segment': 'Dashboard'
    }

    # Page from the theme 
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user_profile = get_or_create_user_profile(request.user.username)
            if len(user_profile.address) == 0 or len(user_profile.city) == 0 or len(user_profile.country_code) == 0 or len(user_profile.phone) == 0 or len(request.user.first_name) == 0 or len(request.user.last_name) == 0:
                return redirect('user_profile')
            else:
                return render(request, 'pages/index.html', context)
        else:
            # Get the current date
            now = timezone.now()
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Monday is considered the start

            #--- Register User Statistic
            total_users = User.objects.count()
            users_joined_this_month = User.objects.annotate(month=TruncMonth('date_joined')).filter(month=timezone.datetime(now.year, now.month, 1)).count()
            users_joined_this_week = User.objects.filter(date_joined__date__gte=start_of_week).count()
            users_joined_today = User.objects.filter(date_joined__date=today).count()
            user_dates = User.objects.aggregate(first_joined=Min('date_joined'), latest_joined=Max('date_joined'))
            first_joined = user_dates['first_joined']
            latest_joined = user_dates['latest_joined']
            # Annotate the queryset with the year and month
            user_counts = User.objects.annotate(
                date=TruncMonth('date_joined')
            ).values('date').annotate(count=Count('id')).order_by('date')

            #--- device type statistic
            device_today = SummaryDevices.objects.filter(tx_date=today).first()
            if device_today:
                device_today_total = device_today.desktop + device_today.mobile + device_today.tablet
                device_today_desktop = device_today.desktop
                device_today_mobile = device_today.mobile
                device_today_tablet = device_today.tablet
            else:
                device_today_total = 0
                device_today_desktop = 0
                device_today_mobile = 0
                device_today_tablet = 0

            #--- Click Summary
            today_tx_sum = ClickSummary.objects.filter(tx_date=today).aggregate(Sum('tx_counted'))
            today_tx_total = today_tx_sum['tx_counted__sum'] or 0
            yesterday = today - timedelta(days=1)  # Get yesterday's date
            yesterday_tx_summary = ClickSummary.objects.filter(tx_date=yesterday).aggregate(Sum('tx_counted'))
            yesterday_tx_total = yesterday_tx_summary['tx_counted__sum'] or 0  # Use 'or 0' to handle case where there are no records for yesterday
            today_delta = yesterday_tx_total - today_tx_total

            samedaylastweek = today - timedelta(days=7)  # Get yesterday's date
            samedaylastweek_tx_summary = ClickSummary.objects.filter(tx_date=samedaylastweek).aggregate(Sum('tx_counted'))
            samedaylastweek_tx_total = samedaylastweek_tx_summary['tx_counted__sum'] or 0  # Use 'or 0' to handle case where there are no records for yesterday

            context = {
                'first_joined': first_joined,
                'latest_joined': latest_joined,
                'total_users': total_users,
                'users_joined_this_month': users_joined_this_month,
                'users_joined_this_week': users_joined_this_week,
                'users_joined_today': users_joined_today,
                'user_counts': user_counts,
                'device_today_total': device_today_total,
                'device_today_desktop': device_today_desktop,
                'device_today_mobile': device_today_mobile,
                'device_today_tablet': device_today_tablet,
                'today_tx_total': today_tx_total,
                'yesterday_tx_total': yesterday_tx_total,
                'today_delta': today_delta,
                'samedaylastweek_tx_total': samedaylastweek_tx_total,
            }
            

            return render(request, 'pages/dashboard-analytics.html', context)
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
                'city': user_profile.city,
                'state_code': user_profile.state_code,
                'country_code': user_profile.country_code,
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
            'parent': 'Account',
            'segment': 'Profile',
            'user': {
                'username': current_user.username,
                'fullname': current_user.first_name + " " + current_user.last_name,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'email': current_user.email,
                'address': user_profile.address,
                'city': user_profile.city,
                'state_code': user_profile.state_code,
                'country_code': user_profile.country_code,
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
    
# Pages for categories
@login_required(login_url="/accounts/login/")
def vacation_rentals(request):
    # Page from the theme 
    return render(request, 'pages/products/product-vacation-rentals.html')

@login_required(login_url="/accounts/login/")
def flights(request):
    # Page from the theme 
    return render(request, 'pages/products/product-flights.html')

@login_required(login_url="/accounts/login/")
def tickets(request):
    # Page from the theme 
    return render(request, 'pages/products/product-tickets.html')

@login_required(login_url="/accounts/login/")
def tours(request):
    # Page from the theme 
    return render(request, 'pages/products/product-tours.html')

@login_required(login_url="/accounts/login/")
def hotels(request):
    # Page from the theme 
    return render(request, 'pages/products/product-hotels.html')

@login_required(login_url="/accounts/login/")
def cars(request):
    # Page from the theme 
    return render(request, 'pages/products/product-cars.html')

@login_required(login_url="/accounts/login/")
def cruises(request):
    # Page from the theme 
    return render(request, 'pages/products/product-cruises.html')

@login_required(login_url="/accounts/login/")
def transfers(request):
    # Page from the theme 
    return render(request, 'pages/products/product-transfers.html')

@login_required(login_url="/accounts/login/")
def activities(request):
    # Page from the theme 
    return render(request, 'pages/products/product-activities.html')

@login_required(login_url="/accounts/login/")
def retail(request):
    # Query the ApplicationToken model to get the token for application 'ACCESSDEAL' and the current user
    cvt, usr, pwd, id = get_credential(request.user, ApplicationChoices.ACCESSDEAL)
    if len(cvt) == 0:
        AccessDev = accessdev.AccessDev()
        cvt = AccessDev.create_member(request.user, ApplicationChoices.ACCESSDEAL)

    context = {
    'cvt': cvt
    }

    # Page from the theme
    ClickDetails.add(request=request, application=ApplicationChoices.ACCESSDEAL, tx_url="https://vacationsavers.enjoymydeals.com/director?cvt="+cvt) 
    return render(request, 'pages/products/product-retails.html', context)

@login_required(login_url="/accounts/login/")
def rails(request):
    # Page from the theme 
    return render(request, 'pages/products/product-rails.html')


@login_required(login_url="/accounts/login/")
def all_in_1(request):
    # Page from the theme 
    return render(request, 'pages/products/product-allinone.html')


# Pages for products
@login_required(login_url="/accounts/login/")
def change_plan(request):
    context = {
    'parent': 'Account',
    'segment': 'Change Plan'
    }

    # Page from the theme 
    return render(request, 'pages/change-plan.html', context)

#########################################################################################################################
#------------------------------------------------------------------------------------------------------------------------<<< timefortickets >>>
@login_required(login_url="/accounts/login/")
def timefortickets(request):
    context = {
    'url': 'https://vacationsavers.timefortickets.com/',
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.TIMETOTICKET, tx_url="https://vacationsavers.timefortickets.com/") 
    return render(request, 'pages/iframe-page.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< tourradar >>>
@login_required(login_url="/accounts/login/")
def tourradar(request):
    context = {
    'url': 'https://vacationsavers.travel.tourradar.com/',
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.TOURRADAR, tx_url="https://vacationsavers.travel.tourradar.com/") 
    return render(request, 'pages/iframe-page.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< flight_vs >>>
@login_required(login_url="/accounts/login/")
def flight_vs(request):
    context = {
    'url': 'https://flights.vacationsavers.com/?cmp=3c26aff8553c068f8857990d2fb95ed447893b85&cmp='+request.user.username,
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.VSFLIGHT, tx_url="https://flights.vacationsavers.com/?cmp=3c26aff8553c068f8857990d2fb95ed447893b85&cmp="+request.user.username) 
    return render(request, 'pages/iframe-page.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< cruise_arrivia >>>
@login_required(login_url="/accounts/login/")
def cruise_arrivia(request):
    Arrivia = arrivia.Arrivia()

    # Get credential from DB
    token, usr, pwd, id = get_credential(request.user, ApplicationChoices.ARRIVIA)
   
    if usr == '':
        #Create Arrivia Default Account
        usr = request.user.email
        pwd = openssl_random_pseudo_bytes(4).hex() + "!A"

        status, message, token, custom1, custom2, custom3 = Arrivia.create_account( user=request.user, username=request.user.username, email=usr, password=pwd )

      
    #Login and GetToken
    status, message, token = Arrivia.get_token( username=request.user.username, email=usr, password=pwd )
    context = {
        'url': "https://members.vacationsavers.com/vacationclub/logincheck.aspx?RedirectURL=%2Fcruises%2F&Token=" + token
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.ARRIVIA, tx_url="https://bookings.vacationsavers.com/vacationclub/logincheck.aspx?RedirectURL=%2Fcruises%2F&Token=" + token) 
    return render(request, 'pages/iframe-page.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< tour_worldia >>>
@login_required(login_url="/accounts/login/")
def tour_worldia(request):

    # Configuration and initialization
    private_key = b'f31eb18475d6ff854b7b5e64698d42fb'  # 32 bytes
    cipher_method = 'AES-256-CBC'

    # User and agency data
    current_user = request.user
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    # Creating "created" for the the query
    created = datetime.utcnow().strftime('%s')  # UNIX timestamp
   
    # Creating "nonce" for the the query
    nonce_bytes = openssl_random_pseudo_bytes(16)
    nonce_hex = nonce_bytes.hex()
    nonce = nonce_hex[:16]
    
     # Creating "digest" for the the query
    email = current_user.email
    data = f"{nonce}{email}{created}{private_key.decode('utf-8')}"

    digest = hashlib.md5(data.encode()).hexdigest()

     # Creating "data" for the query
    user_data = json.dumps({
        'type':'customer',  # or "agent"
        'email':email,
        'first_name':current_user.first_name,
        'last_name':current_user.last_name,
        'phone':user_profile.phone
    })

    # Pad the data before encryption
    encrypted_data = openssl_encrypt(user_data, cipher_method, private_key, nonce.encode())

    query = urlencode({
        'created': created,
        'nonce': nonce,
        'digest':  digest,
        'data': base64.b64encode(encrypted_data.encode())
    })

    context = {
        'url': 'https://vacationsavers.worldia.com/login?' + query,
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.WORLDIA, tx_url="https://vacationsavers.worldia.com/login?" + query) 
    return render(request, 'pages/tour-worldia.html', context)


#------------------------------------------------------------------------------------------------------------------------<<< hotels_booking >>>
@login_required(login_url="/accounts/login/")
def hotels_booking(request):

    context = {
    'usr': request.user.username,
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.BOOKING, tx_url="https://sp.booking.com/gating/authkey?key=ARflaYL1q5&aid=1926534;label=" + request.user.username) 
    return render(request, 'pages/hotels-booking.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< car_access >>>
@login_required(login_url="/accounts/login/")
def car_access(request):
    # Get credential from DB
    cvt, usr, pwd, id = get_credential(request.user, ApplicationChoices.ACCESSIFRAME)
    if len(cvt) == 0:
        AccessDev = accessdev.AccessDev()
        cvt = AccessDev.create_member(request.user, ApplicationChoices.ACCESSIFRAME)

    context = {
    'cvt': cvt
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.ACCESSIFRAME, tx_url="https://booking.accessdevelopment.com/scripts/integration.js?target=divAccess&view=cars&cvt="+cvt) 
    return render(request, 'pages/car-access.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< hotels_access >>>
@login_required(login_url="/accounts/login/")
def hotels_access(request):

    # Get credential from DB
    cvt, usr, pwd, id = get_credential(request.user, ApplicationChoices.ACCESSIFRAME)
    if len(cvt) == 0:
        AccessDev = accessdev.AccessDev()
        cvt = AccessDev.create_member(request.user, ApplicationChoices.ACCESSIFRAME)

    context = {
    'cvt': cvt
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.ACCESSIFRAME, tx_url="https://booking.accessdevelopment.com/scripts/integration.js?target=divAccess&view=hotels&cvt="+cvt) 
    return render(request, 'pages/hotels-access.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< access_travel >>>
@login_required(login_url="/accounts/login/")
def access_travel(request):

    # Get credential from DB
    cvt, usr, pwd, id = get_credential(request.user, ApplicationChoices.ACCESSIFRAME)
    if len(cvt) == 0:
        AccessDev = accessdev.AccessDev()
        cvt = AccessDev.create_member(request.user, ApplicationChoices.ACCESSIFRAME)

    context = {
    'cvt': cvt
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.ACCESSIFRAME, tx_url="https://booking.accessdevelopment.com/scripts/integration.js?target=divAccess&view=activities&cvt="+cvt) 
    return render(request, 'pages/access-travel.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< access_deals >>>
@login_required(login_url="/accounts/login/")
def access_deals(request):

    # Get credential from DB
    cvt, usr, pwd, id = get_credential(request.user, ApplicationChoices.ACCESSDEAL)
    if len(cvt) == 0:
        AccessDev = accessdev.AccessDev()
        cvt = AccessDev.create_member(request.user, ApplicationChoices.ACCESSDEAL)

    context = {
    'cvt': cvt
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.ACCESSDEAL, tx_url="https://vacationsavers.enjoymydeals.com/director?cvt="+cvt) 
    return render(request, 'pages/access-deals.html', context)

#------------------------------------------------------------------------------------------------------------------------<<< gtn >>>
@login_required(login_url="/accounts/login/")
def gtn(request):

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.GTN, tx_url="") 
    return render(request, 'pages/vacation-rentals-gtn.html')

#------------------------------------------------------------------------------------------------------------------------<<< specialdeals >>>
@login_required(login_url="/accounts/login/")
def specialdeals(request):
    context = {
    'url': 'https://www.dunhilltraveldeals.com/api/v1/iframe/5952',
    }

    # Page from the theme 
    ClickDetails.add(request=request, application=ApplicationChoices.DUNHILL, tx_url="https://www.dunhilltraveldeals.com/api/v1/iframe/5952") 
    return render(request, 'pages/iframe-page.html', context)

