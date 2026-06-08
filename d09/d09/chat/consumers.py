import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send message history to the connecting user only
        messages = await self.get_messages()
        for msg in messages:
            await self.send(text_data=json.dumps({
                'username': msg['username'],
                'message': msg['content'],
                'is_join': False,
            }))

        # Broadcast join notification to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': '',
                'message': f'{self.user.username} has joined the chat',
                'is_join': True,
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '').strip()
        if not message:
            return

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': self.user.username,
                'message': message,
                'is_join': False,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
            'is_join': event['is_join'],
        }))

    @database_sync_to_async
    def get_messages(self):
        room = Room.objects.get(name=self.room_name)
        return [
            {'username': m.user.username, 'content': m.content}
            for m in room.messages.select_related('user').all()
        ]

    @database_sync_to_async
    def save_message(self, content):
        room = Room.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=self.user, content=content)
