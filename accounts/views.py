from django.shortcuts import render
from .serializers import RegistrationSerializer
# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class ResgistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.save()
            
            return Response({
                "message":f"{user.phone} registered successfully"
            })
        
        return Response(serializer.errors)
            
            
            
            
            
            
