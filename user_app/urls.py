from rest_framework.routers import DefaultRouter
from django.urls import path, include

from rest_framework import routers
from user_app.views import TrackVS, UnverifiedMentorVS, MentorAV, MentorDetailsAV, TrackVS
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')
router = routers.SimpleRouter()
router.register(r'tracks', TrackVS)
router.register(r'addmentor', UnverifiedMentorVS)


urlpatterns = [
    path('mentors/', MentorAV.as_view(), name='mentor-list'),
    path('mentor/<int:pk>/', MentorDetailsAV.as_view(), name='mentor-detail'),
    path('doc/', schema_view),
    ]
urlpatterns += router.urls