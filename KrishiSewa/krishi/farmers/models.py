from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# products
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

    prod_name = models.CharField(max_length=100, unique=True)
    prod_category = models.CharField(max_length=25, 
                                    choices=types_of_product_choices, 
                                    default="Cereals")
    prod_img = models.ImageField(null=True, upload_to='static/product_images')
    products_for_sales = models.ManyToManyField(User, 
                                                through='ProductsForSale',
                                                related_name='products_for_sale')
    products_production = models.ManyToManyField(User, 
                                                through='Production', 
                                                related_name='products_production')
    products_stock = models.ManyToManyField(User, 
                                            through='ProductStock', 
                                            related_name='products_stock')
    product_home_expense = models.ManyToManyField(User,
                                                  through='HomeExpenses',
                                                  related_name='product_home_expense')
    

# products for sale
class ProductsForSale(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity_in_kg = models.FloatField()
    price_per_kg = models.FloatField()
    added_date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=250, null=True)

    product_comments = models.ManyToManyField(User, 
                                              through='ProductComment', 
                                              related_name='product_comments')
    product_reports = models.ManyToManyField(User, 
                                             through='ProductReport', 
                                             related_name='product_reports')


class ProductComment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductsForSale, on_delete=models.CASCADE, null=True)
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
    reported_product = models.ForeignKey(ProductsForSale, on_delete=models.CASCADE, null=True)
    report_category = models.CharField(max_length=50, choices=categories, default="Misinformation")
    report_description = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)


# production
class Production(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)  # this product_id from Products
    farmer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    production_qty = models.FloatField()
    area = models.FloatField()
    production_date = models.DateTimeField(auto_now_add=True)


class ProductStock(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)   # this product_id from Products
    farmer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stock = models.FloatField()


class ProductSold(models.Model):
    sold_product = models.ForeignKey(ProductsForSale, on_delete=models.SET_NULL, null=True)      # this product_id from ProductsOnSale
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='farmer_id')
    sold_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='buyer_id')
    quantity_sold = models.FloatField()
    sold_price = models.FloatField()
    sold_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=1250, null=True)


class Expenses(models.Model):
    particular = models.CharField(max_length=75)
    category = models.CharField(max_length=50)
    amount = models.FloatField()
    expense_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=150, null=True)
    expense_of = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class HomeExpenses(models.Model):
    categories = [
        ("Consumed", "Consumed"),
        ("Wastes", "Wastes")
    ]

    category = models.CharField(max_length=50, choices=categories, default="Consumed")
    quantity = models.FloatField()
    estimated_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    expense_of = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)




