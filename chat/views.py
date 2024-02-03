from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from chat.models import ChatRoom
from chat.forms import RoomMessageCreateForm, ChatRoomCreateForm


@login_required
def chat(request, room_name="public"):
    chat_room = get_object_or_404(ChatRoom, room_name=room_name)
    message_form = RoomMessageCreateForm()

    chat_room.online_users.add(request.user)

    if request.method == "POST":
        message_form = RoomMessageCreateForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.room = chat_room
            message.save()

            if request.htmx:
                context = {
                    "message": message,
                    "user": request.user,
                }
                return render(request, "chat/partials/message_item.html", context)
            else:
                messages.success(request, "Message sent!")
        else:
            messages.error(request, "Failed to send message. Please try again.")

    context = {
        "chat_messages": chat_room.messages.order_by("timestamp"),
        "room": chat_room,
        "message_form": message_form,
    }

    return render(request, "chat/chat.html", context)


@login_required
def rooms(request):
    room_form = ChatRoomCreateForm()
    all_rooms = ChatRoom.objects.all()
    
    # Show 8 rooms per page
    paginator = Paginator(all_rooms, 8)
    page_number = request.GET.get("page", 1)
    rooms = paginator.get_page(page_number)

    if request.method == "POST":
        if "delete_room" in request.POST:
            room_name = request.POST.get("room_name")
            room = get_object_or_404(ChatRoom, room_name=room_name)
            
            if room.room_name == "public":
                messages.error(request, "The public room cannot be deleted")
                return redirect("rooms")
            
            if room.creator != request.user:
                messages.error(request, "You don't have permission to delete this room")
                return redirect("rooms")
            
            room.delete()
            messages.success(request, f"Room '{room_name}' has been deleted")
            return redirect("rooms")
        else:
            room_form = ChatRoomCreateForm(request.POST)
            if room_form.is_valid():
                room = room_form.save(commit=False)
                room.creator = request.user
                room.save()
                messages.success(request, f"Room '{room.room_name}' has been created!")
                return redirect("chat_room", room_name=room.room_name)
            else:
                for field, errors in room_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

    context = {
        "room_form": room_form,
        "rooms": rooms,
    }

    return render(request, "chat/rooms.html", context)
