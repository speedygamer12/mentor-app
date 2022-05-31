from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from user_app.models import CustomUser, Lead, Mentor, Track

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)

myModels=[Lead, Mentor, Track]
admin.site.register(myModels)