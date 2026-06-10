import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = {}  # room_group_name -> set of usernames

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.room_group_name not in ChatConsumer.connected_users:
            ChatConsumer.connected_users[self.room_group_name] = set()
        ChatConsumer.connected_users[self.room_group_name].add(self.user.username)

        # Send message history to the connecting user only
        messages = await self.get_messages()
        for msg in reversed(messages):
            await self.send(text_data=json.dumps({
                'username': msg['username'],
                'message': msg['content'],
                'is_join': False,
                'is_leave': False,
            }))

        # Broadcast join notification to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': '',
                'message': f'{self.user.username} has joined the chat',
                'is_join': True,
                'is_leave': False,
            }
        )

        # Broadcast updated user list to everyone
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_update',
                'users': list(ChatConsumer.connected_users[self.room_group_name]),
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if self.room_group_name in ChatConsumer.connected_users:
            ChatConsumer.connected_users[self.room_group_name].discard(self.user.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': '',
                'message': f'{self.user.username} has left the chat',
                'is_join': False,
                'is_leave': True,
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'users_update',
                'users': list(ChatConsumer.connected_users.get(self.room_group_name, set())),
            }
        )

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
                'is_leave': False,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
            'is_join': event['is_join'],
            'is_leave': event['is_leave'],
        }))

    async def users_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'users',
            'users': event['users'],
        }))

    @database_sync_to_async
    def get_messages(self):
        room = Room.objects.get(name=self.room_name)
        return [
            {'username': m.user.username, 'content': m.content}
            for m in Message.objects.filter(room=room).select_related('user').order_by('-timestamp')[:3]
        ]

    @database_sync_to_async
    def save_message(self, content):
        room = Room.objects.get(name=self.room_name)
        Message.objects.create(room=room, user=self.user, content=content)
