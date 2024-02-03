from chat.views import chat, rooms
from django.urls import path

urlpatterns = [
    path("", chat, name="chat"),
    path("rooms/", rooms, name="rooms"),
    path("<str:room_name>/", chat, name="chat_room"),
]
