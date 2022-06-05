from rest_framework.routers import DefaultRouter
from django.urls import path, include

from rest_framework import routers
from user_app.views import TrackVS, UnverifiedMentorVS, MentorAV, MentorDetailsAV, TrackVS

router = routers.SimpleRouter()
router.register(r'tracks', TrackVS)
router.register(r'addmentor', UnverifiedMentorVS)


urlpatterns = [
    path('mentors/', MentorAV.as_view(), name='mentor-list'),
    path('mentor/<int:pk>/', MentorDetailsAV.as_view(), name='mentor-detail'),
    ]
urlpatterns += router.urls