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


class Equipment(models.Model):
    types = [
        ("Tractor", "Tractor"),
        ("Harvester", "Harvester"),
        ("ATV or UTV", "ATV or UTV"),
        ("Plows", "Plows"),
        ("Harrows", "Harrows"),
        ("Fertilizer Spreaders", "Fertilizer Spreaders"),
        ("Seeders", "Seeders"),
        ("Balers", "Balers"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=70)
    modal = models.CharField(max_length=50)
    category = models.CharField(max_length=25,
                                choices=types,
                                default="Tractor")
    available_For_Rent = models.BooleanField(default=True)
    available_To_Buy = models.BooleanField(default=True)
    price_To_Buy = models.FloatField()
    price_To_Rent = models.FloatField()
    details = models.CharField(max_length=200)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
