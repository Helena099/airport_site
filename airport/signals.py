from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Passenger
from .email_utils import send_booking_confirmation

@receiver(post_save, sender=Passenger)
def passenger_created_email(sender, instance, created, **kwargs):
    if created:
        send_booking_confirmation(instance)
