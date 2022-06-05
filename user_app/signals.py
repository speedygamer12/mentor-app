from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from .models import Lead, Mentor


def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Lead.objects.create(user=instance)
        if instance.user_type==2:
            Mentor.objects.create(user=instance, gender="", experience="")
        # if instance.user_type==3:
        #     Mentee.objects.create(admin=instance,course_id=Mentee.objects.get(id=1),session_start_year="2020-01-01",
        #     session_end_year="2021-01-01",address="",profile_pic="",gender="")

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)


def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.lead.save()
    if instance.user_type==2:
        instance.mentor.save()
    # if instance.user_type==3:
    #     instance.students.save()

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)