from celery import shared_task
from confluent_kafka import Consumer, KafkaException
from django.conf import settings 
from .services.user_service import UserService
from .services.email_service import send_welcome_email

import logging
import json

logger = logging.getLogger(__name__)

@shared_task
def consume_user_created_topic():
    """
    Celery task to consume messages from the 'user_created' Kafka topic.
    This task runs continuously.
    """
    consumer_config = {
        **settings.KAFKA_CONFIG,  # Reuse Kafka configuration from settings.py
        'group.id': 'user_created_group',  # Add consumer-specific configuration
        'auto.offset.reset': 'earliest',  # Start reading at the earliest message
    }

    consumer = Consumer(consumer_config)
    logger.info("Kafka consumer created with configuration: %s", consumer_config)
    print("Kafka consumer created with configuration:", consumer_config)
    try:
        consumer.subscribe(['user_created'])
        logger.info("Kafka consumer subscribed to topic 'user_created'.")


        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for messages

            if msg is None:
                continue  # No message received, continue polling

            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    # End of partition event
                    logger.info(f"Reached end of partition: {msg.error()}")
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                continue

            # Process the message
            logger.info(f"Received message: {msg.value().decode('utf-8')}")
            process_user_created_message(msg.value().decode('utf-8'))

    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")

def process_user_created_message(message):
    """
    Process the message from the 'user_created' topic.
    Add your custom logic here.
    """
    logger.info(f"Processing message: {message}")

    # Example: Deserialize the message and perform actions
    message_data = json.loads(message)
    logger.info(f"Deserialized message data: {message_data} | Triggering user account creation service.")

    # Call the UserService to create a user account
    user_account = UserService.activate_user_account(message_data)

    if user_account:
        logger.info(f"User account activated successfully: {user_account}")
        # Loosely coupled: trigger async welcome email
        user_email = message_data.get('email')
        user_name = message_data.get('name', 'User')
        send_welcome_email_task.delay(user_email, user_name)
    else:
        logger.error("Failed to activate user account.")
       

@shared_task
def send_welcome_email_task(user_email, user_name):
    send_welcome_email(user_email, user_name)
   