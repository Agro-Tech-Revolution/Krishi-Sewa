from rest_framework.serializers import Serializer
from farmers.serializers import ProductSerializer
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


def modify_product_details_data(product):
    prod_id = product['id']

    product_details = Products.objects.get(id=product['product'])
    product_details_data = ProductSerializer(product_details).data

    user_details = User.objects.get(id=product['added_by'])
    user_details_data = UserSerializer(user_details).data

    comments_details = ProductComment.objects.filter(product=prod_id)
    comments_data = ProductCommentSerializer(comments_details, many=True).data

    for comment in comments_data:
        user_comment_details = User.objects.get(id=comment['comment_by'])
        user_comment_data = UserSerializer(user_comment_details).data
        comment['comment_by'] = user_comment_data

    reports_details = ProductReport.objects.filter(reported_product=prod_id)
    report_data = ProductReportSerializer(reports_details, many=True).data

    for report in report_data:
        user_report_details = User.objects.get(id=report['reported_by'])
        user_report_data = UserSerializer(user_report_details).data
        report['reported_by'] = user_report_data

    product['product'] = product_details_data
    product['added_by'] = user_details_data
    product['product_comments'] = comments_data
    product['product_reports'] = report_data

    return product


def get_product_details(products_for_sale):
    product_data = ProductForSaleSerializer(products_for_sale, many=True).data
        
    for product in product_data:
        product = modify_product_details_data(product)
    return product_data


def modify_production_details_data(production):
    product_details = Products.objects.get(id=production['product_id'])
    product_details_data = ProductSerializer(product_details).data

    farmer_details = User.objects.get(id=production['farmer_id'])
    farmer_details_data = UserSerializer(farmer_details).data

    production['product_id'] = product_details_data
    production['farmer_id'] = farmer_details_data
    return production


def get_production_details(all_production):
    production_data = ProductionSerializer(all_production, many=True).data
        
    for production in production_data:
        production = modify_production_details_data(production)
    return production_data


def modify_product_stock_data(stock_data):
    product_details = Products.objects.get(id=stock_data['product_id'])
    product_details_data = ProductSerializer(product_details).data

    user_details = User.objects.get(id=stock_data['farmer_id'])
    user_details_data = UserSerializer(user_details).data

    stock_data['product_id'] = product_details_data
    stock_data['farmer_id'] = user_details_data
    return stock_data


def get_product_stock_data(product_stock):
    product_stock_data = ProductStockSerializer(product_stock, many=True).data
    for stock_data in product_stock_data:
        stock_data = modify_product_stock_data(stock_data)
    return product_stock_data


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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return Profile.objects.get(user=user_id)
        except Profile.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        profile = self.get_object(user_id)
        profile_data = CreateProfileSerializer(profile).data

        user_details = User.objects.get(id=user_id)
        user_data = UserSerializer(user_details).data
        profile_data['user'] = user_data
        
        return Response(profile_data)


class ProductsAPIView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetails(APIView):
    def get_object(self, id):
        try:
            return Products.objects.get(id=id)
        except Products.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsForSaleView(APIView):
    def get(self, request):
        products_for_sale = ProductsForSale.objects.all()
        product_data = get_product_details(products_for_sale)
        return Response(product_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductForSaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsForSaleDetails(APIView):
    def get_object(self, id):
        try:
            return ProductsForSale.objects.get(id=id)
        except ProductsForSale.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        products_for_sale = self.get_object(id)
        product_for_sale_data = ProductForSaleSerializer(products_for_sale).data
    
        product_data = modify_product_details_data(product_for_sale_data)
        return Response(product_data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        product_for_sale = self.get_object(id)
               
        serializer = ProductForSaleSerializer(product_for_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product_for_sale = self.get_object(id)
        product_for_sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyProductsOnSale(APIView):
    def get_objects(self, user_id):
        try:
            return ProductsForSale.objects.filter(added_by=user_id)
        except ProductsForSale.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        products_for_sale = self.get_objects(user_id)
        product_data = get_product_details(products_for_sale)
        return Response(product_data, status=status.HTTP_200_OK)


class ProductCommentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)    
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
       

class ProductReportView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        reports_details = ProductReport.objects.all()
        report_data = ProductReportSerializer(reports_details, many=True).data

        for report in report_data:
            user_report_details = User.objects.get(id=report['reported_by'])
            user_report_data = UserSerializer(user_report_details).data
            report['reported_by'] = user_report_data

            product_report_details = ProductsForSale.objects.get(id=report['reported_product'])
            product_report_data = ProductForSaleSerializer(product_report_details).data

            product_details = Products.objects.get(id=product_report_data['product'])
            product_details_data = ProductSerializer(product_details).data

            product_report_data['product'] = product_details_data

            report['reported_product'] = product_report_data

        return Response(report_data)
    
    def post(self, request):
        product_id = request.data['reported_product']
        product = Products.objects.get(id=product_id)
        
        serializer = ProductReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ProductionAPIView(APIView):
    def get(self, request):
        all_production = Production.objects.all()
        production_data = get_production_details(all_production)
        return Response(production_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            farmer_id = serializer.data['farmer_id']
            product_id = serializer.data['product_id']
            production_qty = serializer.data['production_qty']
            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(product_stock) != 0:                
                updated_stock = product_stock[0].stock + production_qty
                product_stock.update(stock=updated_stock)
            else:
                farmer = User.objects.get(id=farmer_id)
                product = Products.objects.get(id=product_id)
                ProductStock.objects.create(farmer_id=farmer,
                                            product_id=product,
                                            stock=production_qty)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductionDetails(APIView):
    def get_object(self, id):
        try:
            return Production.objects.get(id=id)
        except Production.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        production_detail = self.get_object(id)
        production_data = ProductionSerializer(production_detail).data
        production_data_to_display = modify_production_details_data(production_data)
        return Response(production_data_to_display, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        production = self.get_object(id)
        prev_production_qty = production.production_qty
        serializer = ProductionSerializer(production, data=request.data)
        if serializer.is_valid():
            serializer.save()
            farmer_id = serializer.data['farmer_id']
            product_id = serializer.data['product_id']
            new_production_qty = serializer.data['production_qty']
            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(product_stock) != 0:                
                updated_stock = product_stock[0].stock + new_production_qty - prev_production_qty
                product_stock.update(stock=updated_stock)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        production = self.get_object(id)
        prev_production_qty = production.production_qty
        farmer_id = production.farmer_id
        product_id = production.product_id
        production.delete()
        
        product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
        if len(product_stock) != 0:                
            updated_stock = product_stock[0].stock - prev_production_qty
            product_stock.update(stock=updated_stock)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyProductions(APIView):
    def get_object(self, user_id):
        try:
            return Production.objects.filter(farmer_id=user_id)
        except Production.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        my_production = self.get_object(user_id)
        production_data = get_production_details(my_production)
        return Response(production_data, status=status.HTTP_200_OK)


class ProductStockAPIView(APIView):
    def get(self, request):
        product_stock = ProductStock.objects.all()
        product_stock_data = get_product_stock_data(product_stock)
        return Response(product_stock_data)


class MyProductStock(APIView):
    def get_object(self, user_id):
        try:
            return ProductStock.objects.filter(farmer_id=user_id)
        except ProductStock.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, user_id):
        product_stock = self.get_object(user_id)
        product_stock_data = get_product_stock_data(product_stock)
        return Response(product_stock_data)

def modify_sold_data(sold_products):
    product_for_sale_details = ProductsForSale.objects.get(id=sold_products['sold_product'])
    product_for_sale_data = SerialzerForSold(product_for_sale_details).data # this is from ProductsForSale

    product_details = Products.objects.get(id=product_for_sale_data['product'])
    product_details_data = ProductSerializer(product_details).data  # this is from Products
    
    farmer_details = User.objects.get(id=sold_products['sold_by'])
    farmer_data = UserSerializer(farmer_details).data

    buyer_details = User.objects.get(id=sold_products['sold_to'])
    buyer_data = UserSerializer(buyer_details).data

    product_for_sale_data['product'] = product_details_data
    sold_products['sold_product'] = product_for_sale_data
    sold_products['sold_by'] = farmer_data
    sold_products['sold_to'] = buyer_data
    return sold_products

def get_sold_details(all_products_sold):
    products_sold_data = ProductSoldSerializer(all_products_sold, many=True).data
    for sold_products in products_sold_data:
        sold_products = modify_sold_data(sold_products)
    return products_sold_data


class ProductSoldView(APIView):
    def get(self, request):
        all_products_sold = ProductSold.objects.all()
        products_sold_data = get_sold_details(all_products_sold)
        return Response(products_sold_data)

    def post(self, request):
        serializer = ProductSoldSerializer(data=request.data)
        if serializer.is_valid():
            farmer_id = request.data["sold_by"]
            product_id = serializer.validated_data["sold_product"].product.id
            
            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)

            if len(product_stock) != 0:
                quantity_sold = request.data['quantity_sold']
                if quantity_sold < product_stock[0].stock:
                    serializer.save()
                    updated_stock = product_stock[0].stock - quantity_sold
                    product_stock.update(stock=updated_stock)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'Bad Request': "The quantity is not available"}, status=status.HTTP_400_BAD_REQUEST)
                        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ProductSoldDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.get(id=id)
        except ProductSold.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        product_sold = ProductSoldSerializer(product_sold_detail).data
        product_sold_data = modify_sold_data(product_sold)
        return Response(product_sold_data)
        

    def put(self, request, id):
        product_sold = self.get_object(id)
        serializer = ProductSoldSerializer(product_sold, data=request.data)

        if serializer.is_valid():
            farmer_id = request.data["sold_by"]
            product_id = serializer.validated_data["sold_product"].product.id
            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(product_stock) != 0:
                current_stock = product_stock[0].stock + product_sold.quantity_sold
                quantity_sold = request.data['quantity_sold']
                if quantity_sold < current_stock:
                    serializer.save()
                    updated_stock = current_stock - quantity_sold
                    product_stock.update(stock=updated_stock)
                    return Response(serializer.data)
                else:
                    return Response({'Bad Request': "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product_sold = self.get_object(id)
        quantity_sold = product_sold.quantity_sold
        farmer_id = product_sold.sold_by
        product_id = product_sold.sold_product.product.id
        product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
        if len(product_stock) != 0:
            current_stock = product_stock[0].stock
            updated_stock = current_stock + quantity_sold
            product_sold.delete()
            product_stock.update(stock=updated_stock)
        return Response(status=status.HTTP_204_NO_CONTENT) 


class SellerSalesDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.get(sold_by=id)
        except ProductSold.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        product_sold = ProductSoldSerializer(product_sold_detail).data
        product_sold_data = modify_sold_data(product_sold)
        return Response(product_sold_data)


class BuyerSalesDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.get(sold_to=id)
        except ProductSold.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        product_sold = ProductSoldSerializer(product_sold_detail).data
        product_sold_data = modify_sold_data(product_sold)
        return Response(product_sold_data)

# equipments
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
        
