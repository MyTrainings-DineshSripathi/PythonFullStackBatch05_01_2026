from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

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
        ("SEEKER", "seeker")
    )

    # Use EmailField for validation and set as unique
    userId = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    fullname = models.CharField(max_length=100)
    company = models.CharField(max_length=50, null=True, blank=True)
    
    # Remove the manual password field; AbstractUser already has it.
    # Remove the username field logic if you want email to be the primary ID
    username = None 
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fullname'] # Do not include 'password' here