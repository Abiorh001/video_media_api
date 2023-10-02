from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_binary', 'video_url', 'transcript', 'last_played', 'created_at']
        read_only_fields = ['last_played', 'created_at', 'video_url']

    def update(self, instance, validated_data):
        # Update the 'transcript' field with plain text data
        instance.transcript = validated_data.get('transcript', instance.transcript)
        instance.save()
        return instance

class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['transcript']
