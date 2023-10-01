
import imageio_ffmpeg as ffmpeg
import subprocess

# Specify input video file and output audio file paths
input_video_path = "/home/abiorh/Videos/Screencasts/scre.webm"
output_audio_path = "/home/abiorh/Videos/Screencasts/"

# Run the ffmpeg command to extract audio
ffmpeg_command = [
    "ffmpeg",
    "-i", input_video_path,
    "-vn",  # Disable video stream
    "-acodec", "libmp3lame",  # Output audio codec (MP3)
    "-q:a", "0",  # Audio quality (0 is the highest)
    output_audio_path
]

try:
    subprocess.run(ffmpeg_command, check=True)
    print("Audio extracted and saved as", output_audio_path)
except subprocess.CalledProcessError as e:
    print("Error extracting audio:", e)
