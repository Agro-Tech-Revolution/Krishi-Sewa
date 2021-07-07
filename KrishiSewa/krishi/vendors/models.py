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
    date = models.DateTimeField(auto_now_add=True)
    eqp_img = models.ImageField(null=True, upload_to='static/equipment_images')
    added_by = models.ForeignKey(User, 
                                 on_delete=models.CASCADE, 
                                 null=True)
    
    comments = models.ManyToManyField(User, 
                                     through='EquipmentComment', 
                                     related_name='eqp_comments')
    reports = models.ManyToManyField(User, 
                                     through='EquipmentReport', 
                                     related_name='eqp_reports')


class EquipmentComment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)


class EquipmentReport(models.Model):
    categories = [
        ("False Information", "False Information"),
        ("Fake Equipments", "Fake Equipments"),
        ("Misinformation", "Misinformation"),
        ("Something Else", "Something Else"),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reported_equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)
    report_category = models.CharField(max_length=50, choices=categories, default="Misinformation")
    report_description = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)