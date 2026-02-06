from django.urls import path,include
from .views import ResgistrationView,LoginView,UserProfileView,LogoutView,ActiveUserAccountView,ForgotPasswordandResendView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('profile',UserProfileView,basename="profile")
urlpatterns = [
    path('registration/',ResgistrationView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name='login'),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("active/",ActiveUserAccountView.as_view(),name="active"),
    path("forgot-password/",ForgotPasswordandResendView.as_view(),name="forgot-password"),
    path("resend-otp-for-account-active/",ForgotPasswordandResendView.as_view(),name="resend-otp"),
    path('',include(router.urls)),
]
