from django.db import models
from django.contrib.auth.models import User
import string
import random

def generate_unique_code():
    length = 8
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if ChatRoom.objects.filter(room_code=code).count() == 0:
            break

    return code

# Create your models here.
class ChatRoom(models.Model):
    room_code = models.CharField(max_length=8, default=generate_unique_code, primary_key=True)
    first_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="first_user")
    second_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="second_user")


class Messages(models.Model):
    room_code = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_by")
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
