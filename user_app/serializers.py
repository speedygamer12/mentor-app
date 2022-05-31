from django.contrib.auth.models import User
from rest_framework import serializers

from user_app.models import Track, Mentor

class MentorSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all(), many=True)

    class Meta:
        model = Mentor
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.tracks = validated_data.get('tracks', instance.tracks)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.save()
        return instance


class LeadMentorSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all(), many=True)

    class Meta:
        model = Mentor
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'