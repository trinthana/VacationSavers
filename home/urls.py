from django.urls import path, re_path

from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('ticket-timefortickets/', views.timefortickets, name='timefortickets'),
    path('tour-radar/', views.tourradar, name='radar'),
    path('flight-smartfares/', views.smartfares, name='smartfares'),
    path('user/profile/', views.profile, name='user_profile'),
    path("delete_account/", views.delete_account, name="delete-account"),
    path('change_plan/', views.change_plan, name='change_plan'),
    path('change_password/', views.change_password, name='changepassword'),
    path('verify-code/', views.verify_code, name='verify_code'),

    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
]


