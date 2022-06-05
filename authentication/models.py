from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"Lead"),(2,"Mentor"),(3,"Mentee"))
    user_type=models.CharField(choices=user_type_data,max_length=10)
    dsnid=models.IntegerField(default=123)

from .signals import create_auth_token
from user_app.signals import create_user_profile, save_user_profile

