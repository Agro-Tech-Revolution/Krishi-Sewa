from operator import mod
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

    name = models.CharField(max_length=70, unique=True)
    category = models.CharField(max_length=25,
                                choices=types,
                                default="Tractor")


class EquipmentToDisplay(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    modal = models.CharField(max_length=75)
    available_for_rent = models.BooleanField(default=False, null=True)
    available_to_buy = models.BooleanField(default=False, null=True)
    price_to_buy_per_item = models.FloatField(null=True)
    price_per_hour = models.FloatField(null=True)
    duration = models.FloatField(null=True) # this can be removed
    details = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    eqp_img = models.CharField(max_length=1200, null=True)
    added_by = models.ForeignKey(User, 
                                 on_delete=models.CASCADE, 
                                 null=True)

    reports = models.ManyToManyField(User, 
                                     through='EquipmentReport', 
                                     related_name='eqp_reports')


class EquipmentReport(models.Model):
    categories = [
        ("False Information", "False Information"),
        ("Fake Equipments", "Fake Equipments"),
        ("Misinformation", "Misinformation"),
        ("Something Else", "Something Else"),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reported_equipment = models.ForeignKey(EquipmentToDisplay, on_delete=models.CASCADE, null=True)
    report_category = models.CharField(max_length=50, choices=categories, default="Misinformation")
    report_description = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)


class BuyDetails(models.Model):
    equipment = models.ForeignKey(EquipmentToDisplay, on_delete=models.SET_NULL, null=True)
    
    sold_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sold_to')
    quantity = models.FloatField()
    delivered_address = models.CharField(max_length=100)
    total_price = models.FloatField()
    sold_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=150, null=True)
    approved = models.BooleanField(default=False)


class RentDetails(models.Model):
    equipment = models.ForeignKey(EquipmentToDisplay, on_delete=models.SET_NULL, null=True)
    
    rented_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rented_to')
    rented_quantity = models.FloatField()
    rented_duration = models.FloatField()
    delivered_address = models.CharField(max_length=100)
    total_price = models.FloatField()
    rented_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=150, null=True)
    approved = models.BooleanField(default=False)
