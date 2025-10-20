# system/utils.py
from django.db.models import Count
from django.utils import timezone
from .models import Chat

def get_or_create_1to1_chat(user_a, user_b):
    """Return (chat, created_bool). Finds a 1-to-1 Chat for the two users or creates it."""
    chat = (Chat.objects.filter(participants=user_a)
                    .filter(participants=user_b)
                    .annotate(num_participants=Count('participants'))
                    .filter(num_participants=2)
                    .first())
    created = False
    if not chat:
        chat = Chat.objects.create(created_at=timezone.now())
        chat.participants.add(user_a, user_b)
        created = True
    return chat, created
