from django.db.models import fields
from rest_framework import serializers
from .models import *

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'category']


class EquipmentToDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentToDisplay
        fields = ['id', 'equipment', 'modal', 'available_for_rent', 'available_to_buy', 'price_to_buy_per_item',
                  'price_per_hour', 'duration', 'details', 'added_by', 'date', 'eqp_img', 'reports']


class EquipmentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentReport
        fields = ['id', 'reported_by', 'reported_equipment', 'report_category', 
                  'report_description', 'reported_date']


class BuyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyDetails
        fields = ['id', 'equipment', 'sold_to', 'quantity', 'delivered_address', 
                  'total_price', 'sold_date', 'remarks', 'approved']


class RentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentDetails
        fields = ['id', 'equipment', 'rented_to', 'rented_quantity', 'delivered_address',
                  'rented_duration', 'total_price', 'rented_date', 'remarks', 'approved']
    
