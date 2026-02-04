from rest_framework import serializers
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException

User=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'phone',
            'country_code',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        phone = attrs.get('phone')
        country_code=attrs.get('country_code')
        print("phone number is ",phone)

        if not password or not confirm_password:
            raise serializers.ValidationError("Password and confirm password are required")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        try:
            phone_number = PhoneNumber.from_string(phone, region=country_code)
            if not phone_number.is_valid():
                raise serializers.ValidationError("Invalid phone number")
            
            if User.objects.filter(phone=phone_number).exists():
                raise serializers.ValidationError("A user with this phone number already exists")
            
        except NumberParseException:
            raise serializers.ValidationError("Invalid phone number or country code")
      
            
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user
        
