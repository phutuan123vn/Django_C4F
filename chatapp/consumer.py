import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import (AsyncWebsocketConsumer,
                                        WebsocketConsumer)

from chatapp.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        date:datetime = await self.insert_message(message)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message,
                                   "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                                   "user": self.user.username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        date:datetime = event["date"]
        user = event["user"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "user": user,
            "message": message,
            "date": date
            }))
        
    @database_sync_to_async
    def insert_message(self,message):
        room = Room.objects.get(pk=int(self.room_name))
        msg = Message.objects.create(room=room, user=self.user, value=message)
        msg.save()
        return msg.date