from rest_framework import serializers
from api.models import *
from admins.models import *
from django.contrib.auth.models import User


class AvailableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'address',
            'contact',
            'user_type',         
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = '__all__'