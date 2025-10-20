# system/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.db.models import Count
from .models import Chat, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_user_id = int(self.scope['url_route']['kwargs']['user_id'])
        self.logged_in_user_id = self.scope['user'].id

        # consistent room name
        room_id = "_".join(sorted([str(self.logged_in_user_id), str(self.other_user_id)]))
        self.room_group_name = f"chat_{room_id}"

        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('message', '').strip()
        if not content:
            return

        sender = self.scope['user']

        # save to DB and get message dict
        message_dict = await self.save_message(sender, self.other_user_id, content)

        # broadcast message payload to group
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message",  # match method name below
            "message": message_dict
        })

    async def chat_message(self, event):
        """
        Add `is_mine` flag based on the current WebSocket connection's user.
        """
        msg = event['message']
        msg['is_mine'] = (msg['sender_id'] == self.logged_in_user_id)
        await self.send(text_data=json.dumps(msg))

    @sync_to_async
    def save_message(self, sender, receiver_id, content):
        receiver = User.objects.get(id=receiver_id)

        # find or create chat with exactly these two participants
        chat = (Chat.objects.filter(participants=sender)
                           .filter(participants=receiver)
                           .annotate(num_participants=Count('participants'))
                           .filter(num_participants=2)
                           .first())
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(sender, receiver)

        msg = Message.objects.create(
            chat=chat,
            sender=sender,
            reciever=receiver,
            content=content,
            timestamp=timezone.now()
        )

        return {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_username": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
        }
