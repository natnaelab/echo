from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import ChatRoom


class Command(BaseCommand):
    help = "Ensures that the public chat room exists"

    def handle(self, *args, **options):
        # Get or create a system user for public room
        system_user, _ = User.objects.get_or_create(
            username="system",
            defaults={
                "is_active": False,
                "is_staff": False,
                "is_superuser": False,
            }
        )

        if not ChatRoom.objects.filter(room_name="public").exists():
            ChatRoom.objects.create(room_name="public", creator=system_user)
            self.stdout.write(self.style.SUCCESS("Created public chat room"))
        else:
            self.stdout.write(self.style.SUCCESS("Public chat room already exists"))
