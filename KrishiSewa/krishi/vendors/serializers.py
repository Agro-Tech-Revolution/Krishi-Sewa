from rest_framework import serializers
from .models import *

class CreateEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'modal', 'category', 'available_for_rent', 'available_to_buy', 'price_to_buy',
                  'price_to_rent', 'details', 'added_by', 'date', 'eqp_img']


class EquipmentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentComment
        fields = ['id', 'comment_by', 'equipment', 'comment', 'comment_date']


class EquipmentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentReport
        fields = ['id', 'reported_by', 'reported_equipment', 'report_category', 
                  'report_description', 'reported_date']