from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin



User = get_user_model()

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the token from the query string and authenticate the user, then try form
        token_key = request.GET.get('auth_token') if request.GET else None
        if not token_key:
            token_key = request.POST.get('auth_token') if request.POST else None
        
        if token_key:
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                # If the token does not exist, ignore or handle as necessary
                pass

        # Proceed with the next middleware or view
        response = self.get_response(request)
        return response
    
    def process_request(self, request):
        print("I am in process_request")
        # Ensure request is not None and has the GET attribute
        if request and hasattr(request, 'GET'):
            # Get the token from the query string
            token_key = request.GET.get('auth_token')
            if token_key:
                try:
                    # Retrieve the token and authenticate the user
                    token = Token.objects.get(key=token_key)
                    request.user = token.user
                except Token.DoesNotExist:
                    # Token is invalid, but proceed with the request
                    pass

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
