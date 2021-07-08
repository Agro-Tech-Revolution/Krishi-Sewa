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
from .utils import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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


class NoteAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

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
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

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
            product_id = request.data['product']
            farmer_id = request.data['added_by']
            quantity_in_kg = float(request.data['quantity_in_kg'])
            
            stock_detail = ProductStock.objects.filter(product_id=product_id, farmer_id=farmer_id)
            if len(stock_detail) != 0:
                if quantity_in_kg < stock_detail[0].stock:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"Bad Request": "The entered quantity is not available. Please check stock value"})
            else:
                return Response({"Bad Request": "The products are not added in production and there is no stock present."})
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

        product_id = request.data['product']
        farmer_id = request.data['added_by']
        quantity_in_kg = float(request.data['quantity_in_kg'])
        
        stock_detail = ProductStock.objects.filter(product_id=product_id, farmer_id=farmer_id)
        if serializer.is_valid():
            if quantity_in_kg < stock_detail[0].stock:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"Bad Request": "The entered quantity is higher than stock value"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response()

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

            # if it is serializer.data no need to add float infront of numbers
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
        prev_production_product_id = production.product_id.id
        serializer = ProductionSerializer(production, data=request.data)
        if serializer.is_valid():  
            farmer_id = request.data['farmer_id']
            product_id = request.data['product_id']
            
            new_production_qty = float(request.data['production_qty'])
            if int(product_id) == prev_production_product_id:
                # if the product is same from previous production then get stock object and
                # update stock value
                product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
                
                if len(product_stock) != 0:                
                    updated_stock = product_stock[0].stock + new_production_qty - prev_production_qty
                    product_stock.update(stock=updated_stock)
    
            else:
                # if the product is not same from previous production
                # updating stock of a previous prdouct which was increased. But now the product name is changed
                # so previous added production quantity to stock is being subtracted
                product_stock_to_update = ProductStock.objects.filter(
                                                                     farmer_id=farmer_id, 
                                                                     product_id=prev_production_product_id
                                                                     )
                stock_of_prev_to_update = product_stock_to_update[0].stock - prev_production_qty
                product_stock_to_update.update(stock=stock_of_prev_to_update)
    
                # finding new product_stock object to update its stock
                product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
                if len(product_stock) != 0:    
                    # if the object exists, update its value            
                    updated_stock = product_stock[0].stock + new_production_qty
                    product_stock.update(stock=updated_stock)
                else:
                    # if the object does not exist, create new stock object
                    farmer = User.objects.get(id=farmer_id)
                    product = Products.objects.get(id=product_id)
                    ProductStock.objects.create(farmer_id=farmer,
                                                product_id=product,
                                                stock=new_production_qty)
            serializer.save()
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
            sold_product = request.data["sold_product"]

            product_to_be_sold = ProductsForSale.objects.filter(id=sold_product)
            quantity_present = product_to_be_sold[0].quantity_in_kg

            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)

            if len(product_stock) != 0:
                quantity_sold = float(request.data['quantity_sold'])
                if quantity_sold < quantity_present:
                    if quantity_sold < product_stock[0].stock:
                        serializer.save()
                        updated_stock = product_stock[0].stock - quantity_sold
                        product_stock.update(stock=updated_stock)

                        updated_quantity = quantity_present - quantity_sold
                        product_to_be_sold.update(quantity_in_kg=updated_quantity)
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
            sold_product = request.data["sold_product"]

            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)

            product_to_be_sold = ProductsForSale.objects.filter(id=sold_product)
            quantity_present = product_to_be_sold[0].quantity_in_kg
            current_qty = quantity_present + product_sold.quantity_sold
            if len(product_stock) != 0:
                current_stock = product_stock[0].stock + product_sold.quantity_sold
                
                quantity_sold = float(request.data['quantity_sold'])
                if quantity_sold < current_qty:
                    if quantity_sold < current_stock:
                        serializer.save()
                        updated_stock = current_stock - quantity_sold
                        product_stock.update(stock=updated_stock)

                        updated_quantity = current_qty - quantity_sold
                        product_to_be_sold.update(quantity_in_kg=updated_quantity)
                        return Response(serializer.data)
                else:
                    return Response({'Bad Request': "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product_sold = self.get_object(id)
        quantity_sold = product_sold.quantity_sold
        farmer_id = product_sold.sold_by
        product_id = product_sold.sold_product.product.id
        sold_product = product_sold.sold_product.id

        product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)

        product_to_be_sold = ProductsForSale.objects.filter(id=sold_product)
        quantity_present = product_to_be_sold[0].quantity_in_kg
        if len(product_stock) != 0:
            current_stock = product_stock[0].stock
            updated_stock = current_stock + quantity_sold
            updated_qty = quantity_present + quantity_sold
            product_sold.delete()
            product_stock.update(stock=updated_stock)
            product_to_be_sold.update(quantity_in_kg=updated_qty)
        return Response(status=status.HTTP_204_NO_CONTENT) 


class SellerSalesDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.filter(sold_by=id)
        except ProductSold.DoesNotExist:
            return None

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        products_sold_data = get_sold_details(product_sold_detail)
        return Response(products_sold_data)
        

class BuyerSalesDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.filter(sold_to=id)
        except ProductSold.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        products_sold_data = get_sold_details(product_sold_detail)
        return Response(products_sold_data)


class ExpenseAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        all_expenses = Expenses.objects.all()
        expense_data = ExpenseSerializer(all_expenses, many=True).data

        for expense in expense_data:
            user_details = User.objects.get(id=expense['expense_of'])
            user_details_data = UserSerializer(user_details).data
            expense['expense_of'] = user_details_data
        return Response(expense_data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, id):
        try:
            return Expenses.objects.get(id=id)
        except Expenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        expense_detail = self.get_object(id)

        expense_data = ExpenseSerializer(expense_detail).data
        user_details = User.objects.get(id=expense_data['expense_of'])
        user_details_data = UserSerializer(user_details).data
        expense_data['expense_of'] = user_details_data

        return Response(expense_data)

    def put(self, request, id):
        expenses = self.get_object(id)
        serializer = ExpenseSerializer(expenses, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        expenses = self.get_object(id)
        expenses.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyExpenses(APIView):
    def get_objects(self, user_id):
        try:
            return Expenses.objects.filter(expense_of=user_id)
        except Expenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        my_expenses = self.get_objects(user_id)
        expense_data = ExpenseSerializer(my_expenses, many=True).data

        for expense in expense_data:
            user_details = User.objects.get(id=expense['expense_of'])
            user_details_data = UserSerializer(user_details).data
            expense['expense_of'] = user_details_data

        return Response(expense_data)


class HomeExpenseAPIView(APIView):
    def get(self, request):
        all_home_expenses = HomeExpenses.objects.all()
        home_expense_data = HomeExpenseSerialer(all_home_expenses, many=True).data

        for expense in home_expense_data:
            user_details = User.objects.get(id=expense['expense_of'])
            user_details_data = UserSerializer(user_details).data
            expense['expense_of'] = user_details_data

            product_details = Products.objects.get(id=expense['product'])
            product_details_data = ProductSerializer(product_details).data
            expense['product'] = product_details_data

        return Response(home_expense_data)

    def post(self, request):
        serializer = HomeExpenseSerialer(data=request.data)

        if serializer.is_valid():
            product_id = request.data["product"]
            farmer_id = request.data["expense_of"]
            stock_detail = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(stock_detail) != 0:
                available_stock = stock_detail[0].stock
                entered_stock = request.data["quantity"]
                if entered_stock < available_stock:
                    updated_stock = available_stock - entered_stock
                    stock_detail.update(stock=updated_stock)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"Bad Request": "Available stock does not match"})
            else:
                return Response({"Bad Request": "No record of this product in production"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeExpenseDetails(APIView):
    def get_object(self, id):
        try:
            return HomeExpenses.objects.get(id=id)
        except HomeExpenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        home_expense_detail = self.get_object(id)

        home_expense_data = HomeExpenseSerialer(home_expense_detail).data

        user_details = User.objects.get(id=home_expense_data['expense_of'])
        user_details_data = UserSerializer(user_details).data
        home_expense_data['expense_of'] = user_details_data

        product_details = Products.objects.get(id=home_expense_data['product'])
        product_details_data = ProductSerializer(product_details).data
        home_expense_data['product'] = product_details_data

        return Response(home_expense_data)

    def put(self, request, id):
        home_expense = self.get_object(id)
        serializer = HomeExpenseSerialer(home_expense, data=request.data)

        if serializer.is_valid():
            product_id = request.data["product"]
            farmer_id = request.data["expense_of"]
            stock_detail = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(stock_detail) != 0:
                available_stock = stock_detail[0].stock + home_expense.quantity
                entered_stock = request.data["quantity"]
                if entered_stock < available_stock:
                    updated_stock = available_stock - entered_stock
                    stock_detail.update(stock=updated_stock)
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"Bad Request": "Available stock does not match"})
            else:
                return Response({"Bad Request": "No record of this product in production"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        home_expenses = self.get_object(id)
        farmer_id = home_expenses.expense_of
        product_id = home_expenses.product
        product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
        current_stock = product_stock[0].stock

        qty_to_remove = home_expenses.quantity
        updated_stock = current_stock + qty_to_remove
        product_stock.update(stock=updated_stock)

        home_expenses.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyHomeExpense(APIView):
    def get_object(self, user_id):
        try:
            return HomeExpenses.objects.filter(expense_of=user_id)
        except HomeExpenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        my_home_expenses = self.get_objects(user_id)
        home_expense_data = HomeExpenseSerialer(my_home_expenses, many=True).data

        for expense in home_expense_data:
            user_details = User.objects.get(id=expense['expense_of'])
            user_details_data = UserSerializer(user_details).data
            expense['expense_of'] = user_details_data

            product_details = Products.objects.get(id=expense['product'])
            product_details_data = ProductSerializer(product_details).data
            expense['product'] = product_details_data

        return Response(home_expense_data)


# equipments
class EquipmentAPIView(APIView):
    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
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
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)

    def put(self, request, id):
        equipment = self.get_object(id)
        serializer = EquipmentSerializer(equipment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        equipment = self.get_object(id)
        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EquipmentsToDisplayView(APIView):
    def get(self, request):
        all_equipments = EquipmentToDisplay.objects.all()
        equipment_data = get_equipment_details(all_equipments)
        return Response(equipment_data)

    def post(self, request):
        serializer = EquipmentToDisplaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentsToDisplayDetails(APIView):
    def get_object(self, id):
        try:
            return EquipmentToDisplay.objects.get(id=id)
        except EquipmentToDisplay.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_detail = self.get_object(id)
        equipment_to_modify = EquipmentToDisplaySerializer(equipment_detail).data
        equipment_data = modify_equipment_detail_data(equipment_to_modify)
        return Response(equipment_data)


    def put(self, request, id):
        equipment_detail = self.get_object(id)
        serializer = EquipmentToDisplaySerializer(equipment_detail, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        equipment_detail = self.get_object(id)
        equipment_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyEquipments(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_objects(self, user_id):
        try:
            return EquipmentToDisplay.objects.filter(added_by=user_id)
        except Equipment.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        equipments = self.get_objects(user_id)
        equipment_data = get_equipment_details(equipments)
        return Response(equipment_data)


# eqp report 
class EquipmentReportView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        reports = EquipmentReport.objects.all()
        serializer = EquipmentReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EquipmentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class BuyEquipmentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        all_buy_details = BuyDetails.objects.all()

        all_buy_data = get_bought_details(all_buy_details)
        return Response(all_buy_data)
    
    def post(self, request):        
        serializer = BuyDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyEquipmentDetails(APIView):
    def get_object(self, id):
        try:
            return BuyDetails.objects.get(id=id)
        except BuyDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        buy_detail = self.get_object(id)
        buy_data_to_modify = BuyDetailsSerializer(buy_detail).data
        buy_data = modify_bought_data(buy_data_to_modify)
        return Response(buy_data)

    def put(self, request, id):
        buy_data = self.get_object(id)
        serializer = BuyDetailsSerializer(buy_data, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        buy_data = self.get_object(id)
        buy_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoughtEquipmentsBuyer(APIView):
    def get_object(self, id):
        try:
            return BuyDetails.objects.filter(sold_to=id)
        except BuyDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_bought_detail = self.get_object(id)
        equipment_bought_data = get_bought_details(equipment_bought_detail)
        return Response(equipment_bought_data)


class SoldEquipmentSeller(APIView):
    def get_object(self, id):
        try:
            return BuyDetails.objects.filter(sold_by=id)
        except BuyDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_bought_detail = self.get_object(id)
        equipment_bought_data = get_bought_details(equipment_bought_detail)
        return Response(equipment_bought_data)


class RentEquipmentView(APIView):
    def get(self, request):
        all_rent_details = RentDetails.objects.all()
        print(all_rent_details[0].rented_by)
        all_rent_data = get_rent_details(all_rent_details)
        return Response(all_rent_data)

    def post(self, request):
        serializer = RentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class RentEquipmentDetails(APIView):
    def get_object(self, id):
        try:
            return RentDetails.objects.get(id=id)
        except RentDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        rent_detail = self.get_object(id)
        rent_data_to_modify = RentDetailsSerializer(rent_detail).data
        rent_data = modify_rented_data(rent_data_to_modify)
        return Response(rent_data)

    def put(self, request, id):
        rent_data = self.get_object(id)
        serializer = RentDetailsSerializer(rent_data, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        rent_data = self.get_object(id)
        rent_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RentedEquipmentsBuyer(APIView):
    def get_object(self, id):
        try:
            return RentDetails.objects.filter(rented_to=id)
        except RentDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_rented_detail = self.get_object(id)
        equipment_rented_data = get_rent_details(equipment_rented_detail)
        return Response(equipment_rented_data)


class RentedEquipmentSeller(APIView):
    def get_object(self, id):
        try:
            return RentDetails.objects.filter(rented_by=id)
        except RentDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_rented_detail = self.get_object(id)
        equipment_rented_data = get_rent_details(equipment_rented_detail)
        return Response(equipment_rented_data)

