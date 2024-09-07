import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db import models
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send past messages to the newly connected user
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'username': message['sender__email'],
                'timestamp': message['timestamp'].isoformat(),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the message to the database
        saved_message = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': self.user.email,
                'timestamp': saved_message.timestamp.isoformat(),
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))

    @database_sync_to_async
    def save_message(self, content):
        recipient = User.objects.get(email=self.room_name)  # Assuming room_name is recipient's email
        return Message.objects.create(sender=self.user, recipient=recipient, content=content)

    @database_sync_to_async
    def get_messages(self):
        recipient = User.objects.get(email=self.room_name)
        messages = Message.objects.filter(
            (models.Q(sender=self.user) & models.Q(recipient=recipient)) |
            (models.Q(sender=recipient) & models.Q(recipient=self.user))
        ).order_by('timestamp').values('content', 'sender__email', 'timestamp')
        return list(messages)