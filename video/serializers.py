from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_binary', 'video_url','is_playing', 'last_played', 'created_at']
        read_only_fields = ['is_playing', 'last_played', 'created_at']