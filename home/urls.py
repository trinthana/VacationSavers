from django.urls import path, re_path

from home import views
from .views import token_login

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('user/profile/', views.profile, name='user_profile'),
    path("delete_account/", views.delete_account, name="delete-account"),
    path('change_plan/', views.change_plan, name='change_plan'),
    path('change_password/', views.change_password, name='changepassword'),
    path('verify-code/', views.verify_code, name='verify_code'),

    path('vacation-rentals/', views.vacation_rentals, name='vacation_rentals'),
    path('flights/', views.flights, name='flights'),
    path('tickets/', views.tickets, name='tickets'),
    path('tours/', views.tours, name='tours'),
    path('hotels/', views.hotels, name='hotels'),
    path('cars/', views.cars, name='cars'),
    path('cruises/', views.cruises, name='cruises'),
    path('transfers/', views.transfers, name='transfers'),
    path('activities/', views.activities, name='activities'),
    path('retail/', views.retail, name='retail'),
    path('rails/', views.rails, name='rails'),
    path('all-in-1/', views.all_in_1, name='all_in_1'),

    path('ticket-timefortickets/', views.timefortickets, name='timefortickets'),
    path('flight-vs/', views.flight_vs, name='flight_vs'),
    path('tour-radar/', views.tourradar, name='radar'),
    path('tour-worldia/', views.tour_worldia, name='tour_worldia'),
    path('tour-getyourguide/', views.tour_getyourguide, name='tour_getyourguide'),
    path('access-travel/', views.access_travel, name='access_travel'),
    path('access-deals/', views.access_deals, name='access_deals'),
    path('cruise-arrivia/', views.cruise_arrivia, name='cruise_arrivia'),
    path('cruise-direct/', views.cruise_direct, name='cruise_direct'),
    path('cruise-redirect/', views.cruise_redirect, name='cruise_redirect'),
    path('car-access/', views.car_access, name='car_access'),
    path('hotels-access/', views.hotels_access, name='hotels_access'),
    path('hotels-booking/', views.hotels_booking, name='hotels_booking'),
    path('resorts-webrez/', views.resorts_webrez, name='resorts_webrez'),
    path('vacation-rentals-gtn/', views.gtn, name='gtn'),
    path('specialdeals/', views.specialdeals, name='specialdeals'),
    path('transfer-talixo/', views.transfer_talixo, name='transfer_talixo'),

    path('token-login/<uuid:token>/', token_login, name='token_login'),
    
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),
]


