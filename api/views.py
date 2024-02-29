from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.access_api import import_access_iframe, import_access_deals, import_access_travel, gen_access_iframe
from rest_framework_multitoken.authentication import MultiTokenAuthentication
from rest_framework_multitoken.utils import get_user_primary_token

# Create your views here.
class DefaultView(APIView):
   
    def get(self, request):
        content = {'Hello': 'Hello, World!'}
        return Response(content)
    
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

class GenToken(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
       
        multi_token = get_user_primary_token(request.user.id)

        content = {'Token': multi_token}
        return Response(content)
