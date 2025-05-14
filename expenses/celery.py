from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import worker_ready

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expenses.settings')

app = Celery('expenses')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY' means all celery-related configs must have the prefix 'CELERY_'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Automatically start the Kafka consumer task when the Celery worker is ready
@worker_ready.connect
def start_kafka_consumer(sender, **kwargs):
    from user.tasks import consume_user_created_topic
    consume_user_created_topic.delay()