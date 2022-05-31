from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"Lead"),(2,"Mentor"),(3,"Mentee"))
    user_type=models.CharField(choices=user_type_data,max_length=10)
    dsnid=models.IntegerField(default=123)

class Lead(models.Model):
    id=models.AutoField(primary_key=True)
    # user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
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
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=10, null=True, blank=True)
    phone = models.IntegerField(default=0, blank=True)
    tracks= models.ManyToManyField(Track, null=True, blank=True)
    experience = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    objects=models.Manager()


class Mentee(models.Model):
    # id=models.AutoField(primary_key=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(blank=True, max_length=10)
    phone = models.IntegerField(blank=True)
    track= models.ForeignKey(Track, on_delete=models.CASCADE)
    experience = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)
    objects=models.Manager()



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Lead.objects.create(user=instance)
        if instance.user_type==2:
            Mentor.objects.create(user=instance, gender="", experience="")
        # if instance.user_type==3:
        #     Mentee.objects.create(admin=instance,course_id=Mentee.objects.get(id=1),session_start_year="2020-01-01",
        #     session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.lead.save()
    if instance.user_type==2:
        instance.mentor.save()
    # if instance.user_type==3:
    #     instance.students.save()