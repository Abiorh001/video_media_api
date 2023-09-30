#!/bin/env python3

import io
import os
# Specify the path to your video file
video_file_path = '/home/abiorh/Downloads/test.mp4'

# Open and read the video file as binary data
with open(video_file_path, 'rb') as video_file:
    video_blob = io.BytesIO(video_file.read())

# Determine where you want to save the Blob data as a file
save_path = '/home/abiorh/Downloads/'  # Replace with your desired directory
os.makedirs(save_path, exist_ok=True)

# Specify the file name for the saved video
file_name = 'saved_video.blob'  # Replace with your desired file name and extension

# Save the Blob data as a file on disk
with open(os.path.join(save_path, file_name), 'wb') as output_file:
    output_file.write(video_blob.getvalue())

# The video is now saved as 'saved_video.blob' in the specified directory


