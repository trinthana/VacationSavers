from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tour-radar/', views.tourradar, name='radar'),
    path('flight-smartfares/', views.smartfares, name='smartfares'),
    
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
]
