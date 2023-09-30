from django.db import models
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_binary = models.BinaryField(blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    audio_file = models.FileField(
        upload_to='audios/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])],
        blank=True,
        null=True
    )
    is_playing = models.BooleanField(default=False)
    last_played = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



class VideoChunk(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    chunk_number = models.IntegerField()
    chunk_file = models.FileField(upload_to='video_chunks/%Y/%m/%d/',
                              validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    audio_chunk_file = models.FileField(upload_to='audio_chunks/%Y/%m/%d/',
                                  validators=[FileExtensionValidator(allowed_extensions=['mp3'])], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
