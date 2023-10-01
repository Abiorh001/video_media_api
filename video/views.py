
import os
import tempfile
import pika
import json
from moviepy.editor import VideoFileClip
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from .models import Video, VideoChunk
from .serializers import VideoSerializer
from django.conf import settings
from django.http import StreamingHttpResponse, FileResponse
from django.shortcuts import get_object_or_404


class Status(APIView):
    def get(self, request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class CreateListVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        response = {
            "status": "success",
            "message": "All Videos retrieved successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request):
        data = request.data
        video_file = data.get('video_binary')
        title = data.get('title')
        description = data.get('description')

        if not video_file:
            response = {
                "status": "error",
                "message": "Blob video is required.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            video_obj = serializer.save()
            video_url = f'https://zuri-stage-6-apis.onrender.com/api/videos/{video_obj.id}/'
            video_obj.video_url = video_url
            video_obj.save()

            try:
                # Create a directory to store video chunks if it doesn't exist
                chunk_directory = os.path.join(settings.MEDIA_ROOT, 'video_chunks', str(video_obj.id))
                os.makedirs(chunk_directory, exist_ok=True)

                audio_chunk_directory = os.path.join(settings.MEDIA_ROOT, 'audio_chunks', str(video_obj.id))
                os.makedirs(audio_chunk_directory, exist_ok=True)

                # Read the binary data from the uploaded file
                video_binary = video_file.read()

                # Create a temporary video file to save the video data
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_video_file:
                    temp_video_file.write(video_binary)
                    temp_video_path = temp_video_file.name

                # Extract audio from the entire video using MoviePy
                video_clip = VideoFileClip(temp_video_path)
                audio_clip = video_clip.audio

                # Save the audio as a temporary audio file (e.g., WAV)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_temp_file:
                    audio_clip.write_audiofile(audio_temp_file.name)
                    audio_temp_file_path = audio_temp_file.name

                # Reset the file pointer to the beginning of the video bytes
                video_file.seek(0)

                chunk_number = 0
                while True:
                    chunk = video_file.read(1024 * 1024)  # Read 1MB at a time (adjust chunk size as needed)
                    if not chunk:
                        break

                    # Save the video chunk as a separate file
                    chunk_filename = f'chunk_{chunk_number}.webm'
                    chunk_path = os.path.join(chunk_directory, chunk_filename)

                    with open(chunk_path, 'wb') as chunk_file:
                        chunk_file.write(chunk)

                    # Create a VideoChunk object for this chunk
                    video_chunk = VideoChunk.objects.create(
                        video=video_obj,
                        chunk_number=chunk_number,
                        chunk_file=chunk_path
                    )
                    video_chunk.save()

                    chunk_number += 1

                # Clean up temporary video file
                os.remove(temp_video_path)

                # Send the path of the temporary audio file to RabbitMQ
                send_audio_file_to_rabbitmq(audio_temp_file_path)

            except Exception as e:
                # Handle errors here
                response = {
                    "status": "error",
                    "message": "Error uploading video chunks.",
                    "data": str(e)
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response = {
                "status": "success",
                "message": "Video uploaded successfully",
                "data": serializer.data
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status": "error",
                "message": "Video not created",
                "data": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


def send_audio_file_to_rabbitmq(audio_file_path):
    try:
        # Set up RabbitMQ connection
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a queue for incoming audio file paths
        channel.queue_declare(queue='audio_file_paths')

        # Send the path of the temporary audio file as a message to RabbitMQ
        channel.basic_publish(exchange='', routing_key='audio_file_paths', body=audio_file_path)

        # Close the connection
        connection.close()

        print("Audio file path sent to RabbitMQ")
    except Exception as e:
        # Handle RabbitMQ connection errors
        print("Error sending audio file path to RabbitMQ:", str(e))


class StreamVideo(APIView):
    def get(self, request: Request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        chunk_file = VideoChunk.objects.filter(video=video).order_by('chunk_number')

        def generate_chunks():
            for chunk in chunk_file:
                yield from chunk.chunk_file.open('rb')
        
        response = FileResponse(generate_chunks(), content_type='video/webm')
    
        # Set the Content-Disposition header for inline content
        response['Content-Disposition'] = f'inline; filename="{video.title}.webm"'
    

        # response = StreamingHttpResponse(file_iterator(), content_type='video/mp4')
        # response['Content-Disposition'] = f'attachment; filename="{video.title}.mp4"'
        return response
