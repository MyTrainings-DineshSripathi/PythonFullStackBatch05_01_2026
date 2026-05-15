from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import os
from datetime import timedelta
from django.utils import timezone
import secrets
import string
import random


def user_profile_picture_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    safe_extension = extension if extension else '.jpg'
    return f'users/user_{instance.userId}/profile{safe_extension}'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # This hashes the password!
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
   
# custom user 
class User(AbstractUser):
    ROLE_CHOICES = (
        ("HR", "hr"),
        ("SEEKER", "seeker"),
        ("ADMIN", "admin")
    )

    # Use EmailField for validation and set as unique
    userId = models.BigAutoField(primary_key=True)
    uid = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_moderator = models.BooleanField(default=False, help_text="Whether user has moderation permissions")
    fullname = models.CharField(max_length=100)
    company = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)
    
    # New fields for job seeker profiles
    bio = models.TextField(null=True, blank=True, help_text="Short bio about yourself")
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    # Experience - stores list of experience objects
    experience = models.JSONField(
        default=list,
        blank=True,
        help_text="List of work experience: [{title, company, start_date, end_date, description, current}]"
    )
    
    # Skills - stores list of skills as strings
    skills = models.JSONField(
        default=list,
        blank=True,
        help_text="List of skills"
    )
    
    # Job preferences - stores user's job search preferences
    job_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Job search preferences: {job_types, locations, experience_level, salary_min, salary_max}"
    )

    # Remove the manual password field; AbstractUser already has it.
    # Remove the username field logic if you want email to be the primary ID
    username = None 
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fullname'] # Do not include 'password' here

    def save(self, *args, **kwargs):
        if not self.uid:
            while True:
                candidate = f"uid{random.randint(1000, 999999)}"
                if not type(self).objects.filter(uid=candidate).exists():
                    self.uid = candidate
                    break
        super().save(*args, **kwargs)


class OTP(models.Model):
    """Model to store OTP tokens for email verification"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=5)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """Check if OTP is still valid and not expired"""
        if self.is_verified:
            return False
        if self.attempts >= self.max_attempts:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    def increment_attempts(self):
        """Increment failed attempt count"""
        self.attempts += 1
        self.save()


class PasswordResetToken(models.Model):
    """Model to store password reset tokens"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_valid(self):
        """Check if token is still valid and not expired"""
        if self.is_used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    @staticmethod
    def generate_token():
        """Generate a secure random token"""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(50))


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user.email} - {self.permission.name}"
