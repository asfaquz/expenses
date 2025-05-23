from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from confluent_kafka import Producer
from .models import User
import json

# Pre-save signal
@receiver(pre_save, sender=User)
def user_pre_save_handler(sender, instance, **kwargs):
    print(f"Pre-save signal triggered for: {instance.id}")


@receiver(post_save, sender=User)
def publish_user_created(sender, instance, created, **kwargs):

    print(f"\n--- SIGNAL TRIGGERED --- USER --- {created}")
    if created:  # Only publish if the user is created
        topic = 'user_created'
        key=str(instance.id)
        action = 'new_user_created'
        message = {
                'id': instance.id,
                'name': instance.first_name + " " + instance.last_name,
                'mobile_number':  instance.mobile_country_code + "-" +instance.mobile_number,
                'email': instance.email,
                'action': action,
                'created_at': str(instance.created_at),
            }
        try:
            producer = Producer({'bootstrap.servers': 'localhost:29092'})
            producer.produce(topic, key=key, value=json.dumps(message))
            producer.flush()
            print(f"Message sent to Kafka topic '{topic}' --- {key} : {message}")
        except Exception as e:
             print(f"Failed to send message to Kafka: {e}")
       