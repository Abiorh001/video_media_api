from django.urls import path
from .views import CreateListVideoView, StreamUpdateDestroyVideoView, Status

urlpatterns = [
    path('videos/', CreateListVideoView.as_view(), name='create-list-video'),
    path('videos/<int:video_id>/', StreamUpdateDestroyVideoView.as_view(), name='update-video-transcript'),
    path('videos/<int:video_id>/', StreamUpdateDestroyVideoView.as_view(), name='stream-video'),
    path('videos/<int:video_id>/', StreamUpdateDestroyVideoView.as_view(), name='delete-video'),
    path('status/', Status.as_view(), name='status'),
 ]
