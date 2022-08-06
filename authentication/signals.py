from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from .models import CustomUser, PhoneModel

def create_phone_model(sender, instance, created, **kwargs):
    PhoneModel.objects.create(user=instance, mobile=instance.phone)

post_save.connect(create_phone_model, sender=CustomUser)
       
def save_phone_model(sender, instance, **kwargs):
    instance.phonemodel.save()

post_save.connect(create_phone_model, sender=CustomUser)