from rest_framework import serializers
from .models import *


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'posted_by', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'prod_name', 'quantity_in_kg', 'prod_category', 
                  'prod_price', 'prod_added_on', 'prod_added_by']


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = ['id', 'comment_by', 'product', 'comment', 'comment_date']


class ProductReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReport
        fields = ['id', 'reported_by', 'reported_product', 'report_category', 
                  'report_description', 'reported_date']
