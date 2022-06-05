from django.contrib import admin

from user_app.models import Lead, Mentor, Track

myModels=[Lead, Mentor, Track]
admin.site.register(myModels)