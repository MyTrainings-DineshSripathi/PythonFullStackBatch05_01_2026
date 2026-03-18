from django.db import models

# Create your models here.
class Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstName = models.CharField(max_length=40, null=False)
    middleName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=40, null=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    phone = models.BigIntegerField(max_length=10, unique=True, null=False)