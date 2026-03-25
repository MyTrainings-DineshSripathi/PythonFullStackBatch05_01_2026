from rest_framework.serializers import Serializer
from .models import User

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

# Fetch the custom User model we defined earlier
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # We set password to write_only so it's never returned in an API response
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['userId', 'email', 'fullname', 'password', 'role', 'company']

    def validate(self, data):
        """
        Custom validation: If the role is HR, ensure a company name is provided.
        """
        if data.get('role') == 'HR' and not data.get('company'):
            raise serializers.ValidationError(
                {"company": "Company name is required for HR registration."}
            )
        print(f"inside the register serializer {data}")
        return data

    def create(self, validated_data):
        """
        Overriding the create method to use our Custom Manager's create_user.
        This ensures the password gets hashed correctly.
        """
        return User.objects.create_user(**validated_data)
    

# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        print(f"login serializer {data}")
        user = authenticate(
            username=data['email'],
            password=data['password']
        )
        
        print(user)
        if not user:
            raise serializers.ValidationError("invalid credentials")
        
        return user