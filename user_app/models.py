from django.conf import settings
from django.db import models

from cloudinary.models import CloudinaryField
from twilio.rest import Client

class Lead(models.Model):
    # id=models.AutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    objects=models.Manager()
    

class Track(models.Model):
    # id=models.AutoField(primary_key=True)
    track_name=models.CharField(max_length=24)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Mentor(models.Model):
    # id=models.AutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender=models.CharField(max_length=10, null=True, blank=True)
    phone = models.IntegerField(default=0, blank=True)
    tracks= models.ManyToManyField(Track, null=True, blank=True)
    experience = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    phone_is_verified = models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    objects=models.Manager()

    image = CloudinaryField("image", blank=True)
    @property
    def image_url(self):
        print(type(self.image))
        return (
            f"https://res.cloudinary.com/dpoix2ilz/{self.image}"
        )


class Mentee(models.Model):
    # id=models.AutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender=models.CharField(blank=True, max_length=10)
    phone = models.IntegerField(blank=True)
    track= models.ForeignKey(Track, on_delete=models.CASCADE)
    experience = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    objects=models.Manager()

