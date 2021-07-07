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
        fields = ['id', 'product', 'added_by', 'quantity_in_kg', 'price_per_kg', 'added_date', 'product_comments', 'product_reports']


class SerialzerForSold(serializers.ModelSerializer):
    class Meta:
        model = ProductsForSale
        fields = ['id', 'product', 'quantity_in_kg', 'price_per_kg']


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
        fields = ['id', 'product_id', 'farmer_id', 'production_qty', 'area', 'production_date']


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['id', 'product_id', 'farmer_id', 'stock']


class ProductSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSold
        fields = ['id', 'sold_product', 'sold_by', 'sold_to', 'quantity_sold', 'sold_price', 'sold_date', 'remarks']
