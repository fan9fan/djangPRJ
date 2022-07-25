from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location_addr = models.CharField(max_length=200)
    post_num = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    web = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    birth_day = models.DateField()
    live_addr = models.CharField(max_length=200)

