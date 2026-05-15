from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
import json

from .password_reset_service import PasswordResetService

# Fetch the custom User model we defined earlier
User = get_user_model()

FREE_EMAIL_DOMAINS = {
    "gmail.com",
    "googlemail.com",
    "yahoo.com",
    "yahoo.co.in",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "msn.com",
    "icloud.com",
    "me.com",
    "mac.com",
    "aol.com",
    "proton.me",
    "protonmail.com",
    "zoho.com",
    "yandex.com",
    "gmx.com",
    "mail.com",
    "rediffmail.com",
}

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

        email = (data.get('email') or '').strip().lower()
        role = data.get('role')

        if role == 'HR':
            domain = email.split('@')[-1] if '@' in email else ''

            if not domain or domain in FREE_EMAIL_DOMAINS:
                raise serializers.ValidationError(
                    {"email": "HR accounts must use an official company email address."}
                )

            if '.' not in domain:
                raise serializers.ValidationError(
                    {"email": "Enter a valid company email domain for HR registration."}
                )
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
        email = (data.get('email') or '').strip().lower()
        user = authenticate(
            username=email,
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("invalid credentials")

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'userId',
            'uid',
            'email',
            'fullname',
            'role',
            'company',
            'phone',
            'bio',
            'location',
            'profile_picture',
            'experience',
            'skills',
            'job_preferences',
        ]

    def get_profile_picture(self, obj):
        if not obj.profile_picture:
            return None
        request = self.context.get('request')
        url = obj.profile_picture.url
        return request.build_absolute_uri(url) if request else url


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'company', 'profile_picture', 'phone', 'bio', 'location', 'experience', 'skills', 'job_preferences']

    def validate(self, data):
        user = self.instance
        role = user.role if user else None
        company = data.get('company', user.company if user else None)

        if role == 'HR' and not company:
            raise serializers.ValidationError(
                {"company": "Company name is required for HR accounts."}
            )

        return data

    def to_internal_value(self, data):
        mutable_data = data.copy()
        for field in ('experience', 'skills', 'job_preferences'):
            value = mutable_data.get(field)
            if isinstance(value, str):
                try:
                    mutable_data[field] = json.loads(value)
                except json.JSONDecodeError:
                    raise serializers.ValidationError({
                        field: "Enter valid JSON data."
                    })
        return super().to_internal_value(mutable_data)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        reset_token = PasswordResetService.get_reset_token(data['token'])
        if not reset_token:
            raise serializers.ValidationError(
                {"token": "Invalid or expired reset token."}
            )

        try:
            validate_password(data['password'], user=reset_token.user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)})

        data['reset_token'] = reset_token
        return data
