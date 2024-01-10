from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.access_api import import_access_member

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
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(import_access_member(''))
    
