from rest_framework import serializers
from api.models import *
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