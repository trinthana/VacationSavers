from django.shortcuts import render
from django.http import HttpResponse

from django import template
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

# Create your views here.

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
