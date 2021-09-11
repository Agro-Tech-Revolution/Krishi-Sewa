from django.db.models import fields
from rest_framework import serializers
from .models import *


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'posted_by', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'prod_name', 'prod_category', 'prod_img']


class ProductForSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsForSale
        fields = ['id', 'product', 'added_by', 'quantity_in_kg', 'price_per_kg', 
                  'added_date', 'details', 'product_comments', 'product_reports']


class SerialzerForSold(serializers.ModelSerializer):
    class Meta:
        model = ProductsForSale
        fields = ['id', 'product', 'quantity_in_kg', 'price_per_kg', 'added_by']


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'comment_by', 'product', 'comment', 'comment_date']


class ProductReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReport
        fields = ['id', 'reported_by', 'reported_product', 'report_category', 
                  'report_description', 'reported_date']


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'product_id', 'farmer_id', 'production_qty', 'area', 'production_date', 'remarks']


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['id', 'product_id', 'farmer_id', 'stock']


class ProductSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSold
        fields = ['id', 'sold_product', 'sold_to', 'quantity_sold', 'sold_price', 'sold_date', 'remarks', 'approved', 'seen']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['id', 'particular', 'expense_type', 'unit', 'quantity', 
                  'amount', 'expense_date', 'remarks', 'expense_of']


class HomeExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeExpenses
        fields = ['id', 'category', 'quantity', 'estimated_price', 'date', 'expense_of', 'product', 'remarks']


class NPKTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPKTest
        fields = '__all__'


class ImageTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTest
        fields = '__all__'