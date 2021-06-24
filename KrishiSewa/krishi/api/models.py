from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=50)
    
    profile_pic = models.ImageField(upload_to='static/profile_pic',
                                    null=True,
                                    default='static/profile_pic/default_profile.jpg')



