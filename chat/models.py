from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class ChatRoom(models.Model):
    room_name = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9-_]+$",
                message="Room name can only contain letters, numbers, hyphens, and underscores",
            ),
        ],
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_rooms")
    online_users = models.ManyToManyField(User, related_name="online_in_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name
    
    @property
    def message_count(self):
        return self.messages.count()

    @property
    def online_user_count(self):
        return self.online_users.count()

    class Meta:
        ordering = ["room_name"]


class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

    class Meta:
        ordering = ["timestamp"]
