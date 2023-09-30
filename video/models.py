from django.db import models
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='videos/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    video_url = models.CharField(max_length=255, blank=True, null=True)
    is_playing = models.BooleanField(default=False)
    last_played = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VideoChunk(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    chunk_number = models.IntegerField()
    chunk_file = models.FileField(upload_to='video_chunks/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    created_at = models.DateTimeField(auto_now_add=True)
