from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException


#Custom User settings

class CustomUserManager(BaseUserManager):

    def create_user(self, phone, country_code, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number must be set")
        if not country_code:
            raise ValueError("The Country Code must be set")

        try:
            phone_number = PhoneNumber.from_string(phone, region=country_code)
            if not phone_number.is_valid():
                raise ValueError("Invalid phone number")
        except NumberParseException:
            raise ValueError("Invalid phone number or country code")

        user = self.model(
            phone=phone_number,
            country_code=country_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, country_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, country_code, password, **extra_fields)


#CustomUser model it's the main model 

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15,unique=True)
    country_code = models.CharField(max_length=5)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['country_code']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

    class Meta:
        ordering = ['-date_joined']
