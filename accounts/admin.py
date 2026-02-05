from django.contrib import admin
from django.contrib.auth import get_user_model
User=get_user_model()
from .models import UserProfile
# Register your models here.

admin.site.register(User)
# admin.site.register(UserProfile)

@admin.register(UserProfile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display=['user__phone','email','name','gender','birth_date']

