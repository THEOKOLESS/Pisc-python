from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room


@login_required(login_url='/account/')
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


@login_required(login_url='/account/')
def room(request, room_name):
    chat_room = get_object_or_404(Room, name=room_name)
    return render(request, 'chat/room.html', {'room': chat_room})
