# Video Upload and Processing API Documentation

This documentation provides an overview of the Python code that implements a Video Upload and Processing API. The code is designed to handle video uploads, extract audio from the uploaded videos, and perform asynchronous audio-to-text transcription using OpenAI's API. Below, you will find a detailed explanation of the code structure, its functionality, and important considerations.

## Table of Contents

- [Introduction](#introduction)
- [Code Structure](#code-structure)
- [API Endpoints](#api-endpoints)
    - [Server Status](#server-status)
    - [List Uploaded Videos](#list-uploaded-videos)
    - [Upload a New Video](#upload-a-new-video)
    - [Stream Uploaded Video](#stream-uploaded-video)
    - [Update Video Transcript](#update-video-transcript)
    - [Delete Uploaded Video](#delete-uploaded-video)
- [Usage Instructions](#usage-instructions)

## Introduction

This Python code provides the backend functionality for a Video Upload and Processing API. It is built using Django and Django REST framework, and it utilizes the MoviePy library for video processing and OpenAI for audio-to-text transcription. The code handles the following key functionalities:

- Uploading video files with titles and descriptions.
- Extracting audio from uploaded videos.
- Storing video chunks and associated metadata.
- Asynchronously transcribing audio to text using OpenAI's API.
- Providing API endpoints for listing, streaming, updating, and deleting videos.

## Code Structure

The code is organized into several parts:

1. **API Endpoints**: Defines API endpoints using Django REST framework to interact with videos.
2. **Models**: Defines the database models for videos and video chunks.
3. **RabbitMQ Integration**: Manages the asynchronous processing of audio files using RabbitMQ and OpenAI.
4. **Settings**: Contains Django settings and configurations.
5. **Main Function**: Initializes the RabbitMQ consumer for audio file processing.

## API Endpoints

### Server Status

- **Endpoint**: `/status/`
- **HTTP Method**: GET
- **Description**: Returns the status of the server.
- **Response**: JSON object with a "status" field indicating "ok" if the server is running.

### List Uploaded Videos

- **Endpoint**: `/videos/`
- **HTTP Method**: GET
- **Description**: Retrieves a list of all uploaded videos.
- **Response**: JSON object with video details, including title, description, and video URL.

### Upload a New Video

- **Endpoint**: `/videos/`
- **HTTP Method**: POST
- **Description**: Uploads a new video with a title, description, and video binary data.
- **Request Body**: JSON object containing title, description, and video binary data.
- **Response**: JSON object with a success message and the video's details if the upload is successful.

### Stream Uploaded Video

- **Endpoint**: `/videos/{video_id}/stream/`
- **HTTP Method**: GET
- **Description**: Streams the uploaded video with the specified ID.
- **Response**: Video stream with the "Content-Disposition" header for inline content.
### Retrieve Uploaded Video

- **Endpoint**: `/videos/{video_id}/`
- **HTTP Method**: GET
- **Description**: Retrieve  the uploaded video with the specified ID.
- **Response**: JSON object with a success message and the video's details if the upload is successful.


### Update Video Transcript

- **Endpoint**: `/videos/{video_id}/`
- **HTTP Method**: PUT
- **Description**: Updates the transcript for the video with the specified ID.
- **Request Body**: JSON object containing the new transcript.
- **Response**: JSON object indicating success or error in updating the transcript.

### Delete Uploaded Video

- **Endpoint**: `/videos/{video_id}/`
- **HTTP Method**: DELETE
- **Description**: Deletes the video with the specified ID.
- **Response**: JSON object indicating success or error in deleting the video.

## Usage Instructions

To use this API, follow these steps:

1. Set up a Django project and configure the database.
2. Install required Python packages using `pip install -r requirements.txt`.
3. Start the Django development server.
4. Make POST requests to `/videos/` to upload videos.
5. Use the provided endpoints to list, stream, update, or delete videos.
6. Ensure RabbitMQ is installed and running to enable asynchronous audio transcription.
7. Run the `consumer_rabbitmq.py` script to consume audio file paths and initiate transcription.

