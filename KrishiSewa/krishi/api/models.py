from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=50)
    contact = models.IntegerField(null=True, blank=True)
    profile_pic = models.CharField(max_length=500,
                                   null=True,
                                   default='static/profile_pic/default_profile.jpg')
    address = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)





