import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import ChatRoom, RoomMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.add_user_to_room()

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "online_users_update", "html": await self.render_online_users()},
        )

    async def disconnect(self, close_code):
        await self.remove_user_from_room()
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "online_users_update", "html": await self.render_online_users()},
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        if message:
            saved_message = await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message_id": saved_message.id},
            )

    async def chat_message(self, event):
        message = await self.get_message(event["message_id"])
        html = await self.render_message(message)
        await self.send(text_data=html)

    async def online_users_update(self, event):
        await self.send(text_data=event["html"])

    @database_sync_to_async
    def add_user_to_room(self):
        room = ChatRoom.objects.get(room_name=self.room_name)
        room.online_users.add(self.user)

    @database_sync_to_async
    def remove_user_from_room(self):
        room = ChatRoom.objects.get(room_name=self.room_name)
        room.online_users.remove(self.user)

    @database_sync_to_async
    def save_message(self, message):
        room = ChatRoom.objects.get(room_name=self.room_name)
        return RoomMessage.objects.create(room=room, user=self.user, message=message)

    @database_sync_to_async
    def get_message(self, message_id):
        return RoomMessage.objects.get(id=message_id)

    @database_sync_to_async
    def render_message(self, message):
        return render_to_string("chat/partials/message.html", {"message": message, "user": self.user})

    @database_sync_to_async
    def render_online_users(self):
        room = ChatRoom.objects.get(room_name=self.room_name)
        users_html = render_to_string(
            "chat/online_users.html",
            {"users": [{"username": user.username} for user in room.online_users.all()]},
        )
        count_html = render_to_string("chat/partials/online_count.html", {"count": room.online_users.count()})
        return users_html + count_html
