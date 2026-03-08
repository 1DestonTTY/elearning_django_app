from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage

@login_required(login_url='/login/')
def index(request):
    return render(request, 'chat/index.html')

@login_required(login_url='/login/')
def room(request, room_name):
    chat_history = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')[:50]
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat_history': chat_history #pass the history to the html
    })