from rest_framework import serializers
from .models import *

class CreateEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'modal', 'category', 'available_for_rent', 'available_to_buy', 'price_to_buy',
                  'price_to_rent', 'details', 'added_by', 'date']