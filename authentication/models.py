from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"Lead"),(2,"Mentor"),(3,"Mentee"))
    user_type=models.CharField(choices=user_type_data,max_length=10)
    dsnid = models.IntegerField(default=123)
    is_verified = models.BooleanField(default=False)
    phone = models.IntegerField()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class PhoneModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='sms')
    mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)

    def __str__(self):
            return str(self.Mobile)

from user_app.signals import create_user_profile, save_user_profile

