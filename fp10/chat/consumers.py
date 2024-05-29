import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        Custom_user = get_user_model()
        user = await self.get_user()
        if user:
            user.online_status = True
            await database_sync_to_async(user.save)()

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
        

        await self.accept()

    async def disconnect(self, close_code):
        print("kullanıcı siteden gitti")
        Custom_user = get_user_model()
        user = await self.get_user()
        if user:
            user.online_status = False
            await database_sync_to_async(user.save)()
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        type_of = text_data_json["type_of"]
        user = self.scope["user"]
        
        # m = Message.objects.create(content = message, user = user, room_id = self.room_name, type_of=type_of)

        await self.save_to_database(message,user,self.room_name,type_of)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "user": user.username, "created_date": self.object_message.get_short_date(), "type_of": type_of}
        )
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_date = event["created_date"]
        type_of = event["type_of"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "user":user, "created_date": created_date, "type_of": type_of}))

    @database_sync_to_async
    def save_to_database(self, message, user, room, type_of):
        m = Message.objects.create(content = message, user = user, room_id = room, type_of=type_of)
        self.object_message = m

    @database_sync_to_async
    def get_user(self):
        Custom_user = get_user_model()
        try:
            return Custom_user.objects.get(username=self.scope['user'])
        except Custom_user.DoesNotExist:
            return None






class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.group_name = 'online_status_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def notify_status_change(self, event):
        
        print("consumers.py")
        print(event["online_status"])
        await self.send(text_data=json.dumps({
            'user': event['user'],
            'online_status': event['online_status']
        }))
