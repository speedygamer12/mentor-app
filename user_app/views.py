from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from user_app.permissions import (IsAdminOrReadOnly, 
                                    IsActiveOwnerorReadOnly)
from user_app.models import Track, Mentor 
from user_app.serializers import (LeadMentorSerializer, TrackSerializer, MentorSerializer)

class TrackVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    
class UnverifiedMentorVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Mentor.objects.filter(is_active=False)
    serializer_class = LeadMentorSerializer

    

class MentorAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        queryset = Mentor.objects.filter(is_active=True)
        serializer = MentorSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MentorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class MentorDetailsAV(APIView):

    permission_classes = [IsActiveOwnerorReadOnly]

    def get(self, request, pk):
        try:
            mentor = Mentor.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            return Response({'Error': 'Mentor not found'}, status = status.HTTP_404_NOT_FOUND)

        serializer = MentorSerializer(mentor, context={'request': request})
        return Response(serializer.data)
        
    def put(self, request, pk):
        try:
            mentor = Mentor.objects.get(pk=pk)
        except Mentor.DoesNotExist:
            return Response({'Error': 'Mentor not found'}, status = status.HTTP_404_NOT_FOUND)

        serializer = MentorSerializer(mentor, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request,pk):
        mentor = Mentor.objects.get(pk=pk)
        mentor.delete()
        content = {'Nothing to see here'}
        return Response(content, status = status.HTTP_204_NO_CONTENT)    