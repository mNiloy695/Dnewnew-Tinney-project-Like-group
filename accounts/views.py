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
from twilio.rest import Client
from django.conf import settings

# from .phone_otp import otp_send
from .task import phone_otp_send

from django.contrib.auth import get_user_model
User=get_user_model()
class ResgistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.save()
            user.is_active=False
            user.save()
            otp_code=randint(1000,9999)
            
            try:
                OTP.objects.create(
                user=user,
                code=otp_code,
                type="active"
            )
                
            except Exception as e:
                print("otp not crate a problem ",{e})
                
            
            print("Here is your otp",otp_code)
            
            #phone_otp_send running in backgroud and it's imported from task.py
            
            message=phone_otp_send.delay(phone=str(user.phone),otp=otp_code,main_message="active you Tinny account")
            
            
            return Response({
                "message": "OTP sent successfully! Check your SMS inbox.",
                
            },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
      
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
            refresh_token=request.data.get("refresh",None)
            if not refresh_token:
                return Response(
                    {"error":"Refresh token not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message":"Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error":"Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)
            
            

from django.utils import timezone

class ActiveUserAccountView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        otp_type = request.data.get("type")
        
        if not phone or not code or not otp_type:
            
            return Response(
                {"error":"phone,code,otp_type  is required"},
            )

        otp = OTP.objects.select_related('user').filter(
            user__phone=phone,
            code=code,
            type=otp_type
        ).first()
        
        print(otp)
      
        if not otp:
            return Response(
                {"error": "OTP is invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if otp.is_expired():
            
            return Response(
                {"error": "OTP is expired"},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        
        
        user = otp.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        
        otp.delete()

        return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)