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
    prod_img = models.ImageField(null=True, upload_to='static/product_images')
    prod_added_by = models.ForeignKey(User, 
                                     on_delete=models.CASCADE, 
                                     null=True,
                                     related_name='prod_added_by')
    comments = models.ManyToManyField(User, 
                                     through='ProductComment', 
                                     related_name='comments')
    reports = models.ManyToManyField(User, 
                                     through='ProductReport', 
                                     related_name='reports')
    

class ProductComment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)


class ProductReport(models.Model):
    categories = [
        ("False Information", "False Information"),
        ("Fake Products", "Fake Products"),
        ("Misinformation", "Misinformation"),
        ("Something Else", "Something Else"),
    ]

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reported_product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    report_category = models.CharField(max_length=50, choices=categories, default="Misinformation")
    report_description = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)
