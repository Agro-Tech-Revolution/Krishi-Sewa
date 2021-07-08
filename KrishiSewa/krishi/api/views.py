from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from rest_framework import status
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class NoteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializers(notes, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetails(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, id):
        try:
            return Note.objects.get(id=id)
        except Note.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        note = self.get_object(id)
        serializer = NoteSerializers(note)
        return Response(serializer.data)

    def put(self, request, id):
        note = self.get_object(id)
        serializer = NoteSerializers(note, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        note = self.get_object(id)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CreateProfile(APIView):
    def post(self, request):
        serializer = CreateProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileType(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return Profile.objects.get(user=user_id)
        except Profile.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        profile = self.get_object(user_id)
        serializer = CreateProfileSerializer(profile)
        return Response(serializer.data)


class CreateEquipment(APIView):
    
    def get(self, request):
        equipment = Equipment.objects.all()
        serializer = CreateEquipmentSerializer(equipment, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = CreateEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentDetails(APIView):

    def get_object(self, id):
        try:
            return Equipment.objects.get(id=id)
        except Equipment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment = self.get_object(id)
        serializer = CreateEquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, id):
        equipment = self.get_object(id)
        serializer = CreateEquipmentSerializer(equipment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        equipment = self.get_object(id)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
