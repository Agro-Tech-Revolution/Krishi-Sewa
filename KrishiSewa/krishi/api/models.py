from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=50)
    contact = models.IntegerField(null=True)
    profile_pic = models.ImageField(upload_to='static/profile_pic',
                                    null=True,
                                    default='static/profile_pic/default_profile.jpg')



