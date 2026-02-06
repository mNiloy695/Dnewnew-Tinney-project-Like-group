from django.urls import path,include
from .views import ResgistrationView,LoginView,UserProfileView,LogoutView,ActiveUserAccountView
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('profile',UserProfileView,basename="profile")
urlpatterns = [
    path('registration/',ResgistrationView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name='login'),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("active/",ActiveUserAccountView.as_view(),name="active"),
    path('',include(router.urls)),
]
