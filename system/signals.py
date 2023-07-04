from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BloodRequest, Notification

@receiver(post_save, sender=BloodRequest)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Get all users who should receive the notification
        users = User.objects.all()

        # Send the notification to each user
        for user in users:
            # Create a new notification instance
            notification = Notification(
                user=user,
                blood_request=instance,
                message="A new blood request has been submitted."
            )
            notification.save()
