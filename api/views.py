from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_multitoken.models import MultiToken



from api.authentication import IsValidUserToken
from app.access_api import import_access_iframe, import_access_deals, import_access_travel, gen_access_iframe
from app.models import UserProfile, SubscriptionHistory, PackageChoices

from datetime import datetime, timedelta

# Create your views here.
class DefaultView(APIView):
   
    def get(self, request):
        content = {'Hello': 'Hello, World!'}
        return Response(content)

class CreateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    def post(self, request, format=None):
        # At this point, the token is already validated
        # You can now proceed to create the user or perform other actions
        session_token = request.META.get('HTTP_AUTHORIZATION')
        
        # Create UserProfile data with PREMIER subscription plan
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.subscribed_package = PackageChoices.PREMIER
        user_profile.subscribed_date = datetime.now()
        user_profile.expired_date = datetime.now() + timedelta(days=365)
        user_profile.token = session_token
        user_profile.save()

        # Dummy implementation of user creation
        username = request.user.username
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        #user = User.objects.create(username=username)
        return Response({"message": "User created successfully", "user_id": username}, status=status.HTTP_201_CREATED)

    def get(self, request):
        username = request.user.username
        
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        #user = User.objects.create(username=username)
        return Response({"message": "User created successfully", "user_id": username}, status=status.HTTP_201_CREATED)



class GenTokens(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    def post(self, request, format=None):
        # At this point, the token is already validated
        # You can now proceed to create the user or perform other actions
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the number of tokens to generate from the querystring
        number = request.query_params.get('number', 1)
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the number is within a reasonable limit to prevent abuse
        if number <= 0 or number > 1000:
            return Response({"error": "Number of tokens must be between 1 and 100"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate and save the specified number of tokens
        tokens = []
        for _ in range(number):
            token = MultiToken(user=user)
            token.save()  # The token key will be generated in the save method
            tokens.append(token.key)

        # Return the generated tokens
        return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)

    def get(self, request):
        # At this point, the token is already validated
        # You can now proceed to create the user or perform other actions
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the number of tokens to generate from the querystring
        number = request.query_params.get('number', 1)
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid 'number' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the number is within a reasonable limit to prevent abuse
        if number <= 0 or number > 1000:
            return Response({"error": "Number of tokens must be between 1 and 100"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate and save the specified number of tokens
        tokens = []
        for _ in range(number):
            token = MultiToken(user=user)
            token.save()  # The token key will be generated in the save method
            tokens.append(token.key)

        # Return the generated tokens
        return Response({"tokens": tokens}, status=status.HTTP_201_CREATED)




#---------- Playground : can be deleted ------------------
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class GenAccess(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(gen_access_iframe(''))

class GenAccess1(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(import_access_iframe(''))
    
class GenAccess2(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(import_access_travel(''))

class GenAccess3(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(import_access_deals(''))

