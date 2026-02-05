from django.shortcuts import render
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import token_blacklist
from random import randint

class ResgistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.save()
            otp_code=randint(1000,9999)
            
            try:
                OTP.objects.create(
                user=user,
                code=otp_code
            )
            except Exception as e:
                print("otp not crate a problem ",{e})
                
            return Response({
                "message":f"{user.phone} registered successfully"
            })
        
        return Response(serializer.errors)
            
      
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data["user"]
            
            refresh=RefreshToken.for_user(user)
            
            return Response(
                {
                    "message":"User login sucessfully",
                     "user":{
                         "id":user.id,
                         "username":user.username,
                         "phone":user.phone,
                         "email":user.email,
                         "birth_date":user.birth_date
                     },
                     "refresh":str(refresh),
                     "access":str(refresh.access_token)
                }
            )
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
from .serializers import UserProfileSerializer
from .models import UserProfile



class CustomProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user==obj.user


class UserProfileView(ModelViewSet):
    queryset=UserProfile.objects.select_related("user")
    serializer_class=UserProfileSerializer
    permission_classes=[permissions.IsAuthenticated,CustomProfilePermission]
    
    def get_queryset(self):
        user=self.request.user
        if not user.is_staff:
            return self.queryset.filter(user=user)
        return self.queryset
     






#Logout View

class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message":"Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error":"Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
