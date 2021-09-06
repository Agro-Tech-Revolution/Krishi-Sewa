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
    
    my_chat = ChatRoom.objects.filter(Q(first_user=first_user) | Q(second_user=first_user))
    my_messages = []
    for chat in my_chat:
        get_message = Messages.objects.filter(room_code=chat.room_code).order_by('-sent_date')
        if len(get_message) > 0:
            message = get_message[0].message
        else:
            message = ""
        if chat.first_user == first_user:
            chat_with = chat.second_user
        elif chat.second_user == first_user:
            chat_with = chat.first_user
        my_messages.append({"user": chat_with, "message": message})
    
    return render(request, 'chat/chatbox.html', {
        'room_name': room_name,
        'messages_sent': messages_sent,
        'sent_by': second_user,
        "my_messages": my_messages

    })

def test(request):
    return render(request, 'chat/chatbox.html')