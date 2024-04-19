from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_multitoken.models import MultiToken

from drf_spectacular.utils import extend_schema
from api.authentication import IsValidUserToken
from app.models import UserProfile, SubscriptionHistory, PackageChoices
from app.serializers import UserSerializer, UserTokenSerializer, CreateUserSerializer, ResponseUserSerializer, RequestSerializer, ResponseSerializer, StatusSerializer


from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin

from datetime import datetime, timedelta

# Create your views here.
@xframe_options_sameorigin
def home(request):
    return render(request, 'pages/doc.html')

@xframe_options_sameorigin
def api_content(request):
    return render(request, 'pages/content.html')

class DefaultView(APIView):
   
    def get(self, request):
        content = {'Hello': 'Hello, World!'}
        return Response(content)

class CreateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request=CreateUserSerializer, responses=ResponseUserSerializer)
    def post(self, request, *args, **kwargs):
        # At this point, the token is already validated
        # You can now proceed to create the user or perform other actions
        session_token = request.auth.key
        current_user = request.user
        
        # Create UserProfile data with PREMIER subscription plan
        serializer = UserSerializer(data=request.data, context={'token': session_token})
        if serializer.is_valid():
            try:
                user = serializer.save()
                # Optionally return the generated password or remove this line to keep it secret
                token, created = Token.objects.get_or_create(user=user)
                response_data = serializer.data
                response_data['password'] = user.password  # Note: This will be the hashed password, not the plain text
                response_data['token'] = token.key
                return Response(response_data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # Handle the IntegrityError
                if 'username' in str(e):
                    return Response({'error': 'A user with that username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'email' in str(e):
                    return Response({'error': 'A user with that email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Handle other IntegrityError cases
                    return Response({'error': 'An error occurred during user creation.'}, status=status.HTTP_400_BAD_REQUEST)
                 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAuthToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request= RequestSerializer, responses=ResponseSerializer)
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        session_token = request.auth.key

        if not username:
            return Response({'error': 'Username is required to get inqure token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Attempt to fetch the existing User
                user = User.objects.get(username=username)
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.token != session_token:
                    return Response({'error': 'Either authorization token or username is invalid'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_202_ACCEPTED)                
            except User.DoesNotExist:
                return Response({'error': 'Username does not exist in VacationSavers syystem.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f"Error creating/updating UserProfile: {e}")
                return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

class GetUserList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request="", responses=ResponseUserSerializer)
    def post(self, request, *args, **kwargs):
        
        session_token = request.auth.key
        try:
            user_profile = UserProfile.objects.get(token=session_token)
            serializer = UserTokenSerializer(user_profile.user)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Invalid session token.'}, status=status.HTTP_404_NOT_FOUND)

class DeactivateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request= RequestSerializer, responses=StatusSerializer)
    def post(self, request, *args, **kwargs):
        session_token = request.auth.key
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.token != session_token:
                return Response({'error': 'Either authorization token or username is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.is_active = False
                user.save()
                return Response({'status': 'User ' + username + ' deactivated'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ReactivateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request= RequestSerializer, responses=StatusSerializer)
    def post(self, request, *args, **kwargs):
        session_token = request.auth.key
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.token != session_token:
                return Response({'error': 'Either authorization token or username is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.is_active = True
                user.save()
                return Response({'status': 'User ' + username + ' Reactivated'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class GenTokens(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsValidUserToken]

    @extend_schema(request= RequestSerializer, responses=ResponseUserSerializer)
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

    @extend_schema(request= RequestSerializer, responses=ResponseUserSerializer)
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

def generate_token(request):
    user = request.user  # Assumes the user is already authenticated
    if not user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    
    #token, created = Token.objects.get_or_create(user=user)
    token = MultiToken(user=user)
    token.save()  # The token key will be generated in the save method
    return JsonResponse({'token': token.key})


#---------- Playground : can be deleted ------------------
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

