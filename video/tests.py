import pika
import requests

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a queue for incoming audio data
channel.queue_declare(queue='audio_data')

# Callback for processing incoming messages
def process_audio_data(ch, method, properties, body):
    # Send audio data to Whisper AI for transcription
    audio_data = body
    transcription = send_audio_to_whisper_ai(audio_data)

    # Process the transcription as needed (e.g., save to a database)
    print("Transcription:", transcription)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set up the message consumer
channel.basic_consume(queue='audio_data', on_message_callback=process_audio_data)

print("Waiting for audio data. To exit, press CTRL+C")
channel.start_consuming()

def send_audio_to_whisper_ai(audio_data):
    # Use the Whisper AI API to send audio data and receive transcription
    # Replace with your actual API endpoint and authentication
    url = "https://whisper-ai-api.example.com/transcribe"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    data = {"audio": audio_data}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("transcription")
    else:
        print("Error:", response.text)
        return None
