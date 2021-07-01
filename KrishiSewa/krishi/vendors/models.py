from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    available_for_rent = models.BooleanField(default=True, null=True)
    available_to_buy = models.BooleanField(default=True, null=True)
    price_to_buy = models.FloatField(null=True)
    price_to_rent = models.FloatField(null=True)
    details = models.CharField(max_length=200)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)