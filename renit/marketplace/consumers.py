import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Item, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'chat_{self.item_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        sender_id = self.scope['user'].id
        receiver_id = data['receiver_id']

        message = await self.create_message(sender_id, receiver_id, self.item_id, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': sender_id,
                    'receiver': receiver_id,
                    'content': content,
                    'timestamp': message.timestamp.isoformat(),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    @database_sync_to_async
    def create_message(self, sender_id, receiver_id, item_id, content):
        return Message.objects.create(
            sender=User.objects.get(id=sender_id),
            receiver=User.objects.get(id=receiver_id),
            item=Item.objects.get(id=item_id),
            content=content
        )