# Generated by Django 4.2.5 on 2023-09-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_audio_file_videochunk_audio_chunk_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video',
        ),
        migrations.AddField(
            model_name='video',
            name='video_base64',
            field=models.BooleanField(default=False),
        ),
    ]
