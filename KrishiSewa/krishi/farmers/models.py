from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Products(models.Model):
    types_of_product_choices = [
        ("Cereals", "Cereals"),
        ("Pulses", "Pulses"),
        ("Vegetables", "Vegetables"),
        ("Fruits", "Fruits"),
        ("Nuts", "Nuts"),
        ("Oilseeds", "Oilseeds"),
        ("Sugars and Starches", "Sugars and Starches"),
        ("Fibres", "Fibres"),
        ("Beverages", "Beverages"),
        ("Narcotics", "Narcotics"),
        ("Spices", "Spices"),
        ("Condiments", "Condiments"),
        ("Others", "Others"),
    ]


    prod_name = models.CharField(max_length=100)
    quantity_in_kg = models.FloatField()
    prod_category = models.CharField(max_length=25, 
                                    choices=types_of_product_choices, 
                                    default="Cereals")
    prod_price = models.FloatField()
    prod_added_on = models.DateTimeField(auto_now_add=True)
    prod_added_by = models.ForeignKey(User, 
                                     on_delete=models.CASCADE, 
                                     null=True)
