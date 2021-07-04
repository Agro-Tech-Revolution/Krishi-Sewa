from farmers.views import products
from re import S
from django.db.models import manager
from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from vendors.models import *
from farmers.models import *
from rest_framework import status
from .serializers import *
from farmers.serializers import *
from vendors.serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


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


class UserById(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        user = self.get_object(id)
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


class ProductAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    parser_classes = (MultiPartParser, FormParser)        
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProducts(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_objects(self, user_id):
        try:
            return Products.objects.filter(prod_added_by=user_id)
        except Products.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        products = self.get_objects(user_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, prod_id):
        try:
            return Products.objects.get(id=prod_id)
        except Products.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, prod_id):
        product = self.get_object(prod_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, prod_id):
        product = self.get_object(prod_id)
        if product.prod_added_by.id == request.user.id:
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Bad Request": "Not your product"}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, prod_id):
        product = self.get_object(prod_id)
        
        if product.prod_added_by.id == request.user.id:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Bad Request": "Not your product"}, status=status.HTTP_400_BAD_REQUEST)


class ProductCommentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        comments = ProductComment.objects.all()
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, com_id):
        try:
            return ProductComment.objects.get(id=com_id)
        except ProductComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, com_id):
        comment = self.get_object(com_id)
        serializer = ProductCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, com_id):
        comment = self.get_object(com_id)
               
        serializer = ProductCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def delete(self, request, com_id):
        comments = self.get_object(com_id)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       


class CommentOfProduct(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, prod_id):
        try:
            return ProductComment.objects.filter(product=prod_id)
        except ProductComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, prod_id):
        comments = self.get_object(prod_id)
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentsOnMyProduct(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return ProductComment.objects.filter(product__prod_added_by=user_id)
        except ProductComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        comments = self.get_object(user_id)
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)


class ProductReportView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        reports = ProductReport.objects.all()
        serializer = ProductReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        product_id = request.data['reported_product']
        product = Products.objects.get(id=product_id)
        
        serializer = ProductReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportsOnProduct(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return ProductReport.objects.filter(reported_product=id)
        except ProductReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        reports = self.get_object(id)
        serializer = ProductReportSerializer(reports, many=True)
        return Response(serializer.data)


class ProductReportByUser(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, user_id):
        try:
            return ProductReport.objects.filter(reported_by=user_id)
        except ProductReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        reports = self.get_object(user_id)
        serializer = ProductReportSerializer(reports, many=True)
        return Response(serializer.data)


class ReportDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return ProductReport.objects.get(id=id)
        except ProductReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        report = self.get_object(id)
        serializer = ProductReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, id):
        report = self.get_object(id)
        
        serializer = ProductReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):
        report = self.get_object(id)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class CreateEquipment(APIView):
    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = CreateEquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# equipments
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


class MyEquipments(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_objects(self, user_id):
        try:
            return Equipment.objects.filter(added_by=user_id)
        except Equipment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        equipments = self.get_objects(user_id)
        serializer = CreateEquipmentSerializer(equipments, many=True)
        return Response(serializer.data)


# equipments comments
class EquipmentCommentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        eqp_comments = EquipmentComment.objects.all()
        serializer = EquipmentCommentSerializer(eqp_comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EquipmentCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EqpCommentDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, com_id):
        try:
            return EquipmentComment.objects.get(id=com_id)
        except EquipmentComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, com_id):
        comment = self.get_object(com_id)
        serializer = EquipmentCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, com_id):
        comment = self.get_object(com_id)
        
        serializer = EquipmentCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, com_id):
        comments = self.get_object(com_id)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentOfEquipment(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, eqp_id):
        try:
            return EquipmentComment.objects.filter(equipment=eqp_id)
        except EquipmentComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, eqp_id):
        comments = self.get_object(eqp_id)
        serializer = EquipmentCommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentsOnMyEquipment(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return EquipmentComment.objects.filter(equipment__added_by=user_id)
        except EquipmentComment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        comments = self.get_object(user_id)
        serializer = EquipmentCommentSerializer(comments, many=True)
        return Response(serializer.data)

# eqp report 
class EquipmentReportView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        reports = EquipmentReport.objects.all()
        serializer = EquipmentReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        equipment_id = request.data['reported_equipment']
        equipment = Equipment.objects.get(id=equipment_id)
        
        serializer = EquipmentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportsOnEquipment(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return EquipmentReport.objects.filter(reported_equipment=id)
        except EquipmentReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        reports = self.get_object(id)
        serializer = EquipmentReportSerializer(reports, many=True)
        return Response(serializer.data)


class EquipmentReportByUser(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, user_id):
        try:
            return EquipmentReport.objects.filter(reported_by=user_id)
        except EquipmentReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        reports = self.get_object(user_id)
        serializer = EquipmentReportSerializer(reports, many=True)
        return Response(serializer.data)


class EqpReportDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return EquipmentReport.objects.get(id=id)
        except EquipmentReport.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        report = self.get_object(id)
        serializer = EquipmentReportSerializer(report)
        return Response(serializer.data)

    def put(self, request, id):
        report = self.get_object(id)
        
        serializer = EquipmentReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):
        report = self.get_object(id)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
