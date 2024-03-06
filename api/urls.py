from django.urls import path, re_path

from api import views

urlpatterns = [
    path('', views.DefaultView.as_view(), name='default'),
    path('CreateUser/', views.CreateUser.as_view(), name='CreateUser'),
    path('GetAuthToken/', views.DefaultView.as_view(), name='GetAuthToken'),
    path('DeactivateUser/', views.DefaultView.as_view(), name='DeactivateUser'),
    path('ReActivateUser/', views.DefaultView.as_view(), name='ReActivateUser'),
    path('GetUserList/', views.DefaultView.as_view(), name='GetUserList'),
   path('GenTokens/', views.GenTokens.as_view(), name='GemTokens'),


    # Tghe below is just a playground, can be deleted anytime
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('gen_access/', views.GenAccess.as_view(), name='gen_access'),
    path('gen_access1/', views.GenAccess1.as_view(), name='gen_access1'),
    path('gen_access2/', views.GenAccess2.as_view(), name='gen_access2'),
    path('gen_access3/', views.GenAccess3.as_view(), name='gen_access3'),
 
]


