from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token

class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']

        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
            }, 
            'email':{
                'required': True
            }, 
            'username':{
                'required': True
            }, 
            'first_name':{
                'required': True
            },
            'last_name':{
                'required': True
            }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
               
        return user



class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'user_type']
