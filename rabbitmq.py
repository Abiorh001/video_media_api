import pika
import os
import requests
import openai


openai.api_key = "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"

  
def process_audio_file_path(ch, method, properties, body):
    audio_file_path = body.decode('utf-8')

    # Read the audio file
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    print(transcript)


    

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_audio_paths_from_rabbitmq():
    # Set up RabbitMQ connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue for incoming audio file paths
    channel.queue_declare(queue='audio_file_paths')

    # Set up the message consumer
    channel.basic_consume(queue='audio_file_paths', on_message_callback=process_audio_file_path)

    print("Waiting for audio file paths. To exit, press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_audio_paths_from_rabbitmq()
