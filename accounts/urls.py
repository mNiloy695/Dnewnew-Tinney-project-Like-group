from django.urls import path
from .views import ResgistrationView
urlpatterns = [
    path('registration/',ResgistrationView.as_view(),name="register"),
    
]
