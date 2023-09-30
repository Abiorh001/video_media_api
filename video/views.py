from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Video, VideoChunk
from .serializers import VideoSerializer
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
from django.http import StreamingHttpResponse, FileResponse
from django.shortcuts import get_object_or_404


class Status(APIView):
    def get(self, request):
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class CreateListVideo(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request: Request):
        data = request.data
        video = data.get('video')
        title = data.get('title')
        description = data.get('description')

        if not video:
            response = {
                "status": "error",
                "message": "Video file is required.",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = VideoSerializer(data=data)
        if serializer.is_valid():
            video_obj = serializer.save()
            video_url = f'https://zuri-stage-6-api.onrender.com/api/videos/{video_obj.id}/'
            video_obj.video_url = video_url
            video_obj.save()
               
            try:
                # Create a directory to store video chunks if it doesn't exist
                chunk_directory = os.path.join(settings.MEDIA_ROOT, 'video_chunks', str(video_obj.id))
                os.makedirs(chunk_directory, exist_ok=True)

                chunk_number = 0
                while True:
                    chunk = video.read(1024 * 1024)  # Read 1MB at a time (adjust chunk size as needed)
                    if not chunk:
                        break

                    # Save the video chunk as a separate file
                    chunk_filename = f'chunk_{chunk_number}.mp4'
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
        

class StreamVideo(APIView):
    def get(self, request: Request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        chunk_file = VideoChunk.objects.filter(video=video).order_by('chunk_number')

        def generate_chunks():
            for chunk in chunk_file:
                yield from chunk.chunk_file.open('rb')
        
        response = FileResponse(generate_chunks(), content_type='video/mp4')
    
        # Set the Content-Disposition header for inline content
        response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
    

        # response = StreamingHttpResponse(file_iterator(), content_type='video/mp4')
        # response['Content-Disposition'] = f'attachment; filename="{video.title}.mp4"'
        return response
