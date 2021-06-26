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
