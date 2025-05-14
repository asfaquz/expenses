# Expenses Management System

This project is a Django-based **Expenses Management System** that integrates with **Kafka** for asynchronous message processing and **Celery** for task management. It allows for efficient handling of user-related events and background tasks.

---

## Features

- **User Management**: Handles user creation and updates.
- **Kafka Integration**: Publishes user creation events to a Kafka topic (`user_created`).
- **Celery Integration**: Consumes messages from Kafka and processes them asynchronously.
- **Redis**: Used as the message broker for Celery.
- **Signal Handling**: Automatically triggers Kafka producers on user creation.

---

## Project Structure

expenses/ ├── expenses/ # Main Django project folder │ ├── init.py # Project initialization │ ├── settings.py # Django settings │ ├── urls.py # URL routing │ ├── celery.py # Celery configuration ├── user/ # User app │ ├── models.py # User model │ ├── tasks.py # Celery tasks (Kafka consumer) │ ├── signals.py # Signal handlers (Kafka producer) │ ├── views.py # Views for user management ├── manage.py # Django management script

---

## Requirements

- Python 3.8+
- Django 4.x
- Kafka
- Redis
- Celery
- Confluent Kafka Python Library

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/expenses.git
   cd expenses

2. Create a Virtual Environment:
    python3 -m venv venv
    source venv/bin/activate

3. Install Dependencies
    pip install -r requirements.txt

4. Set Up Kafka:

    Install and start Kafka.
    Ensure the user_created topic exists

    kafka-topics --bootstrap-server localhost:29092 --create --topic user_created --partitions 1 --replication-factor 1

5. Set Up Redis:
    Install and start Redis:
        sudo apt install redis
        redis-server

6. Run Migrations:
    python manage.py migrate

7. Start the Django Development Server:
    python manage.py runserver


Running Celery and Kafka

1. Start the Celery Worker:
    celery -A expenses worker --loglevel=info

2. Start the Kafka Consumer Task: The Kafka consumer task (consume_user_created_topic) will automatically start when the Celery worker starts.

How It Works
User Creation:

When a new user is created, the post_save signal triggers the publish_user_created function.
This function publishes a message to the Kafka topic user_created.
Kafka Consumer:

The consume_user_created_topic Celery task continuously listens to the user_created topic.
When a message is received, it processes the message asynchronously.


Configuration
Kafka Configuration
Update the Kafka settings in settings.py:

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': 'django-producer'
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
