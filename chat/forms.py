from django.forms import ModelForm
from django import forms
from chat.models import RoomMessage, ChatRoom


class RoomMessageCreateForm(ModelForm):
    class Meta:
        model = RoomMessage
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Type your message ...",
                    "class": "w-full resize-none rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 p-3 pr-12",
                    "rows": 1,
                    "maxlength": 1000,
                }
            )
        }


class ChatRoomCreateForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["room_name"]
        widgets = {
            "room_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter room name",
                    "class": "w-full p-3 border border-gray-200 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500",
                }
            )
        }
