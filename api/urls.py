from django.urls import path, re_path

from api import views

urlpatterns = [
    path('', views.DefaultView.as_view(), name='default'),
    path('hello/', views.HelloView.as_view(), name='hello'),

]


