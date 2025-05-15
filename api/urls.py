from django.urls import path, re_path

from api import views

from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='default'),
    path('api_content', views.api_content, name='api_content'),
    path('CreateUser/', views.CreateUser.as_view(), name='CreateUser'),
    path('GetAuthToken/', views.GetAuthToken.as_view(), name='GetAuthToken'),
    path('DeactivateUser/', views.DeactivateUser.as_view(), name='DeactivateUser'),
    path('ReActivateUser/', views.ReactivateUser.as_view(), name='ReActivateUser'),
    path('GetUserList/', views.GetUserList.as_view(), name='GetUserList'),
    path('GenTokens/', views.GenTokens.as_view(), name='GemTokens'),
    path('GenToken/', views.generate_token, name='generate_token'),
    path('subscribe/', views.SubscribeView.as_view(), name='Subscribe'),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('doc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
 
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


