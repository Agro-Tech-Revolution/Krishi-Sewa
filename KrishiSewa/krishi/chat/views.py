from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def room(request, username):
    first_user = User.objects.filter(username=request.user)[0]

    second_user = User.objects.filter(username=username)
    if len(second_user)==0:
        return redirect("/login/")
    else:
        second_user = second_user[0]

    chat_room_obj = ChatRoom.objects.filter(
                                            Q(first_user=first_user, second_user=second_user) | 
                                            Q(first_user=second_user, second_user=first_user)
                                            )
    
    if len(chat_room_obj) == 0:
        chat_room = ChatRoom.objects.create(first_user=first_user, second_user=second_user)
        room_name = chat_room.room_code
        messages_sent = []
    else:
        room_name = chat_room_obj[0].room_code
        messages_sent = Messages.objects.filter(room_code=room_name)

    return render(request, 'chat/chatroom.html', {
        'room_name': room_name,
        'messages_sent': messages_sent
    })