from django.urls import path, re_path

from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tour-radar/', views.tourradar, name='radar'),
    path('flight-smartfares/', views.smartfares, name='smartfares'),
    path('user/profile/', views.profile, name='user_profile'),
    path('change_password/', views.change_password, name='change_password'),

    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
]
