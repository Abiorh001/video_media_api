from django.urls import path
from .views import CreateListVideo, StreamVideo

urlpatterns = [
    path('videos/', CreateListVideo.as_view(), name='create-list-video'),
    path('videos/<int:video_id>/', StreamVideo.as_view(), name='stream-video'),
]