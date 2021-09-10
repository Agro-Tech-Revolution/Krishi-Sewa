from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from vendors.models import *
from farmers.models import *
from django.db.models import Q
from rest_framework import status
from .serializers import *
from farmers.serializers import *
from vendors.serializers import *
from .utils import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django_filters import rest_framework as filters


class FeedbackView(APIView):
    def get(self, request):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    # serializer_class = ChangePasswordSerializer
    # model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, request):
        obj = request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return None

    def get(self, request, username):
        user = self.get_object(username)
        if user != None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({})


class UserById(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request, id):
        user = self.get_object(id)
        if user != None:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({})

    
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
            return None

    def get(self, request, user_id):
        profile = self.get_object(user_id)
        if profile != None:
            profile_data = CreateProfileSerializer(profile).data

            user_details = User.objects.get(id=user_id)
            user_data = UserSerializer(user_details).data
            profile_data['user'] = user_data
            
            return Response(profile_data)
        else:
            return Response({})


class UpdateProfileView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return Profile.objects.get(user=user_id)
        except Profile.DoesNotExist:
            return None

    def put(self, request, user_id):
        profile = self.get_object(user_id)
        if profile != None:
            user = User.objects.get(id=user_id)

            profile_serializer = UpdateProfileSerializer(profile, data=request.data)
            user_serializer = UpdateUserSerializer(user, data=request.data)
            if profile_serializer.is_valid() and user_serializer.is_valid():
                
                profile_serializer.save()
                user_serializer.save()
                return Response(user_serializer.data)
            return Response({"Bad Request": "Cannot update profile"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})


class GetUserDetails(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user_id)
            report_data = ReportUser.objects.filter(reported_user=user_id)

            user_serializer = UpdateUserSerializer(user)
            profile_serializer = UpdateProfileSerializer(profile)
            report_serializer = ReportUserSerializer(report_data, many=True)

            user_dict = user_serializer.data
            profile_dict = profile_serializer.data
            report_dict = report_serializer.data
            user_dict.update(profile_dict)
            user_dict["reports"] = report_dict
            
            if profile.user_type.upper() == 'FARMERS':
                user_dict["total_sales"] = 0
                user_dict["total_purchase"] = 0
            elif profile.user_type.upper() == 'VENDORS':
                user_dict["total_sales"] = 0
                user_dict["total_rent"] = 0
            elif profile.user_type.upper() == 'BUYERS':
                user_dict["total_purchase"] = 0

            

            user_dict["user_type"] = profile.user_type.lower()

            return Response(user_dict)
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)


class ReportUserView(APIView):
    def get(self, request):
        report_user = ReportUser.objects.all()
        serializer = ReportUserSerializer(report_user, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = ReportUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return None

    def get(self, request, id):
        note = self.get_object(id)
        if note != None:
            serializer = NoteSerializers(note)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, id):
        note = self.get_object(id)
        if note != None:
            serializer = NoteSerializers(note, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({})

    def delete(self, request, id):
        note = self.get_object(id)
        if note != None:
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class ProductList(APIView):
    def get(self, request):
        prod_name = request.data.get('prod_name')
        if prod_name is None:
            prod_name = ''
        products_for_sale = ProductsForSale.objects.filter(to_display=True, product__prod_name__icontains=prod_name)

        product_data = get_product_details(products_for_sale)
        return Response(product_data, status=status.HTTP_200_OK)                                                               


class ProductsForSaleView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get(self, request):
        products_for_sale = ProductsForSale.objects.filter(to_display=True)
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
            return None
    
    def get(self, request, id):
        products_for_sale = self.get_object(id)
        if products_for_sale != None:
            if products_for_sale.to_display:
                product_for_sale_data = ProductForSaleSerializer(products_for_sale).data
            
                product_data = modify_product_details_data(product_for_sale_data)
                return Response(product_data, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})
    
    def put(self, request, id):
        product_for_sale = self.get_object(id)
        if product_for_sale != None:
            if product_for_sale.to_display:
                    
                serializer = ProductForSaleSerializer(product_for_sale, data=request.data)

                product_id = request.data['product']
                farmer_id = request.data['added_by']
                quantity_in_kg = float(request.data['quantity_in_kg'])
                
                stock_detail = ProductStock.objects.filter(product_id=product_id, farmer_id=farmer_id)
                if len(stock_detail) > 0:
                    if serializer.is_valid():
                        if quantity_in_kg <= stock_detail[0].stock:
                            serializer.save()
                            return Response(serializer.data)
                        else:
                            return Response({"Bad Request": "The entered quantity is higher than stock value"})
                else:
                    return Response({"Bad Request": "The product has no stock value. Make sure you have added this product to production."})
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})
        

    def delete(self, request, id):
        product_for_sale = ProductsForSale.objects.filter(id=id)
        if len(product_for_sale) != None:
            product_for_sale.update(to_display=False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class MyProductsOnSale(APIView):
    def get_objects(self, user_id):
        try:
            return ProductsForSale.objects.filter(added_by=user_id, to_display=True)
        except ProductsForSale.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        products_for_sale = self.get_objects(user_id)
        if len(products_for_sale) > 0:
            product_data = get_product_details(products_for_sale)
        else:
            product_data = {}
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
            return None
    
    def get(self, request, com_id):
        comment = self.get_object(com_id)
        if comment != None:
            serializer = ProductCommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, com_id):
        comment = self.get_object(com_id)
        if comment != None:
            serializer = ProductCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, com_id):
        comments = self.get_object(com_id)
        if comments != None:
            comments.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})
       

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

            total_report_counts = len(product_report_data["product_reports"])

            product_report_data['product'] = product_details_data

            report['reported_product'] = product_report_data
            report["total_reports"] = total_report_counts
        return Response(report_data)
    
    def post(self, request):        
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
            return None
    
    def get(self, request, id):
        report = self.get_object(id)
        if report != None:
            serializer = ProductReportSerializer(report)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, id):
        report = self.get_object(id)
        if report != None:
        
            serializer = ProductReportSerializer(report, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})
        

    def delete(self, request, id):
        report = self.get_object(id)
        if report != None:
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


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
            return None
    
    def get(self, request, id):
        production_detail = self.get_object(id)
        if production_detail != None:
            production_data = ProductionSerializer(production_detail).data
            production_data_to_display = modify_production_details_data(production_data)
            return Response(production_data_to_display, status=status.HTTP_200_OK)
        else:
            return Response({})
    
    def put(self, request, id):
        production = self.get_object(id)
        if production != None:
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
                        if updated_stock < 0:
                            return Response({"Bad Request": "The quantity you are trying to update for this production has already been sold. Please enter less qunatity values."})
                        else:
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
                    if stock_of_prev_to_update >= 0:
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
                    else:
                        return Response({"Bad Request": "The production of previous product is already used. So cannot update the value."})
                serializer.save()
                return Response(serializer.data)   

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        production = self.get_object(id)
        prev_production_qty = production.production_qty
        farmer_id = production.farmer_id
        product_id = production.product_id
        production.delete()
        
        product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
        if len(product_stock) != 0:                
            updated_stock = product_stock[0].stock - prev_production_qty
            if updated_stock < 0:
                return Response({"Bad Request": "The production has already been sold. You cannot delete this production now."})
            else:
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

# sold product start
class ProductSoldView(APIView):
    def get(self, request):
        all_products_sold = ProductSold.objects.all()
        products_sold_data = get_sold_details(all_products_sold)
        return Response(products_sold_data)

    def post(self, request):
        serializer = ProductSoldSerializer(data=request.data)
        if serializer.is_valid():
            # farmer_id = request.data["sold_by"]
            
            product_id = serializer.validated_data["sold_product"].product.id
            sold_product = request.data["sold_product"]
            farmer_id = serializer.validated_data["sold_product"].added_by.id

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
            # farmer_id = request.data["sold_by"]
            product_id = serializer.validated_data["sold_product"].product.id
            sold_product = request.data["sold_product"]
            farmer_id = serializer.validated_data["sold_product"].added_by.id

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
        farmer_id = product_sold.sold_product.added_by.id
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
            return ProductSold.objects.filter(sold_product__added_by=id)
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
# sold product end


class ExpenseAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        all_expenses = Expenses.objects.all()
        expense_data = get_expense_details(all_expenses)
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
            return None

    def get(self, request, id):
        expense_detail = self.get_object(id)
        if expense_detail != None:
            expense_data = ExpenseSerializer(expense_detail).data
            expense_data = modify_expense_details(expense_data)

            return Response(expense_data)
        else:
            return Response({})

    def put(self, request, id):
        expenses = self.get_object(id)
        if expenses != None:
            serializer = ExpenseSerializer(expenses, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        expenses = self.get_object(id)
        if expenses != None:
            expenses.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class MyExpenses(APIView):
    def get_objects(self, user_id):
        try:
            return Expenses.objects.filter(expense_of=user_id)
        except Expenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        my_expenses = self.get_objects(user_id)
        expense_data = get_expense_details(my_expenses)

        return Response(expense_data)


class HomeExpenseAPIView(APIView):
    def get(self, request):
        all_home_expenses = HomeExpenses.objects.all()
        home_expense_data = get_home_expense_details(all_home_expenses)

        return Response(home_expense_data)

    def post(self, request):
        serializer = HomeExpenseSerializer(data=request.data)

        if serializer.is_valid():
            product_id = request.data["product"]
            farmer_id = request.data["expense_of"]
            stock_detail = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            if len(stock_detail) != 0:
                available_stock = stock_detail[0].stock
                entered_stock = float(request.data["quantity"])
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
            return None

    def get(self, request, id):
        home_expense_detail = self.get_object(id)
        if home_expense_detail != None:
            home_expense_data = HomeExpenseSerializer(home_expense_detail).data

            home_expense_data = modify_home_expense_data(home_expense_data)

            return Response(home_expense_data)
        else:
            return Response({})

    def put(self, request, id):
        home_expense = self.get_object(id)
        if home_expense != None:
            prev_product = home_expense.product.id
            serializer = HomeExpenseSerializer(home_expense, data=request.data)
            
            if serializer.is_valid():
                product_id = request.data["product"]
                farmer_id = request.data["expense_of"]
                stock_detail = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id) # stock detail of present product
                if len(stock_detail) != 0:            
                    if int(product_id) == int(prev_product):
                        
                        available_stock = stock_detail[0].stock + home_expense.quantity
                        entered_stock = float(request.data["quantity"])
                        if entered_stock < available_stock:
                            updated_stock = available_stock - entered_stock
                            if updated_stock >= 0:
                                stock_detail.update(stock=updated_stock)
                            else:
                                return Response({"Bad Request": "Not enough stock available"})
                        else:
                            return Response({"Bad Request": "Available stock does not match"})
                    else:
                        
                        new_updated_stock = stock_detail[0].stock - float(request.data["quantity"])
                        if new_updated_stock >= 0:
                            prev_product_stock_detail = ProductStock.objects.filter(farmer_id=farmer_id, product_id=prev_product)
                            stock_of_prev_to_update = prev_product_stock_detail[0].stock + home_expense.quantity
                            prev_product_stock_detail.update(stock=stock_of_prev_to_update)

                            stock_detail.update(stock=new_updated_stock)
                        else:
                            return Response({"Bad Request": "Not enough stock available"})
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"Bad Request": "No record of this product in production"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        home_expenses = self.get_object(id)
        if home_expenses != None:

            farmer_id = home_expenses.expense_of
            product_id = home_expenses.product
            product_stock = ProductStock.objects.filter(farmer_id=farmer_id, product_id=product_id)
            current_stock = product_stock[0].stock

            qty_to_remove = home_expenses.quantity
            updated_stock = current_stock + qty_to_remove
            product_stock.update(stock=updated_stock)

            home_expenses.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class MyHomeExpense(APIView):
    def get_object(self, user_id):
        try:
            return HomeExpenses.objects.filter(expense_of=user_id)
        except HomeExpenses.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        my_home_expenses = self.get_object(user_id)
        home_expense_data = get_home_expense_details(my_home_expenses)

        return Response(home_expense_data)


# equipments
class EquipmentList(APIView):
    def get(self, request):
        eqp_name = request.data.get('eqp_name')
        if eqp_name is None:
            eqp_name = ''
        eqp_for_sale = EquipmentToDisplay.objects.filter(to_display=True, equipment__name__icontains=eqp_name)

        eqp_data = get_equipment_details(eqp_for_sale)
        return Response(eqp_data, status=status.HTTP_200_OK)  

class EquipmentsToDisplayView(APIView):
    def get(self, request):
        all_equipments = EquipmentToDisplay.objects.filter(to_display=True)
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
            return None

    def get(self, request, id):
        equipment_detail = self.get_object(id)
        if equipment_detail != None:
            if equipment_detail.to_display:
                equipment_to_modify = EquipmentToDisplaySerializer(equipment_detail).data
                equipment_data = modify_equipment_detail_data(equipment_to_modify)
                return Response(equipment_data)
            else: 
                return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


    def put(self, request, id):
        equipment_detail = self.get_object(id)
        if equipment_detail != None:
            if equipment_detail.to_display:
                
                serializer = EquipmentToDisplaySerializer(equipment_detail, data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})

    def delete(self, request, id):
        equipment_detail = EquipmentToDisplay.objects.filter(id=id)
        if len(equipment_detail) != 0:
            equipment_detail.update(to_display=False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class MyEquipments(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    def get_objects(self, user_id):
        try:
            return EquipmentToDisplay.objects.filter(added_by=user_id, to_display=True)
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
        reports_details = EquipmentReport.objects.all()
        report_data = EquipmentReportSerializer(reports_details, many=True).data

        for report in report_data:
            user_report_details = User.objects.get(id=report['reported_by'])
            user_report_data = UserSerializer(user_report_details).data
            report['reported_by'] = user_report_data

            equipment_report_details = EquipmentToDisplay.objects.get(id=report['reported_equipment'])
            equipment_report_data = EquipmentToDisplaySerializer(equipment_report_details).data

            equipment_details = Equipment.objects.get(id=equipment_report_data['equipment'])
            equipment_details_data = EquipmentSerializer(equipment_details).data

            total_report_counts = len(equipment_report_data["reports"])

            equipment_report_data['equipment'] = equipment_details_data

            report['reported_equipment'] = equipment_report_data
            report["total_reports"] = total_report_counts

        return Response(report_data)
    
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
            return None
    
    def get(self, request, id):
        report = self.get_object(id)
        if report != None:
            serializer = EquipmentReportSerializer(report)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, id):
        report = self.get_object(id)
        if report != None:
            serializer = EquipmentReportSerializer(report, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})


    def delete(self, request, id):
        report = self.get_object(id)
        if report != None:
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


# eqp comment 
class EquipmentCommentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)    
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
            return None
    
    def get(self, request, com_id):
        comment = self.get_object(com_id)
        if comment != None:
            serializer = EquipmentCommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, com_id):
        comment = self.get_object(com_id)
        if comment != None:
            serializer = EquipmentCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, com_id):
        comments = self.get_object(com_id)
        if comments != None:
            comments.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})
  

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
            return None

    def get(self, request, id):
        buy_detail = self.get_object(id)
        if buy_detail != None:
            
            buy_data_to_modify = BuyDetailsSerializer(buy_detail).data
            buy_data = modify_bought_data(buy_data_to_modify)
            return Response(buy_data)
        else:
            return Response({})

    def put(self, request, id):
        buy_data = self.get_object(id)
        if buy_data != None:
            if not buy_data.seen: 
                serializer = BuyDetailsSerializer(buy_data, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Bad Request": "This request has already been seen. Cannot update."})
        else:
            return Response({})


    def delete(self, request, id):
        buy_data = self.get_object(id)
        if buy_data != None:
            if not buy_data.approved:
                buy_data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Bad Request": "This request has already been approved. Cannot Delete."})
        else:
            return Response({})
            

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
            return BuyDetails.objects.filter(equipment__added_by=id)
        except BuyDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_bought_detail = self.get_object(id)
        equipment_bought_data = get_bought_details(equipment_bought_detail)
        return Response(equipment_bought_data)


class RentEquipmentView(APIView):
    def get(self, request):
        all_rent_details = RentDetails.objects.all()
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
            return None

    def get(self, request, id):
        rent_detail = self.get_object(id)
        if rent_detail != None:
            rent_data_to_modify = RentDetailsSerializer(rent_detail).data
            rent_data = modify_rented_data(rent_data_to_modify)
            return Response(rent_data)
        else:
            return Response({})

    def put(self, request, id):
        rent_data = self.get_object(id)
        if rent_data != None:
            if not rent_data.seen:
                serializer = RentDetailsSerializer(rent_data, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Bad Request": "This request has already been seen. Cannot update."})
        else:
            return Response({})

    def delete(self, request, id):
        rent_data = self.get_object(id)
        if rent_data != None:
            if not rent_data.approved:
                rent_data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Bad Request": "This request has already been approved. Cannot Delete"})
        else:
            return Response({})


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
            return RentDetails.objects.filter(equipment__added_by=id)
        except RentDetails.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        equipment_rented_detail = self.get_object(id)
        equipment_rented_data = get_rent_details(equipment_rented_detail)
        return Response(equipment_rented_data)


class ProfitLossReportView(APIView):
    def get(self, request, id):
        # income
        product_sales_details = ProductSold.objects.filter(sold_product__added_by=id)
        product_sold_data = get_sold_details(product_sales_details)
        total_income = 0
        for sale in product_sold_data:
            product_name = sale["sold_product"]["product"]["prod_name"]
            prod_seller_fname = sale["sold_to"]["first_name"]
            prod_seller_lname = sale["sold_to"]["last_name"]

            sale["date"] = sale["sold_date"]
            sale["particular"] = product_name + " to " + prod_seller_fname + " " + prod_seller_lname
            sale["quantity"] = sale["quantity_sold"]
            sale["price"] = sale["sold_price"]
            sale["user"] = sale["sold_by"]
            
            total_income += sale["sold_price"]

            sale.pop("sold_product", None)
            sale.pop("sold_by", None)
            sale.pop("sold_to", None)
            sale.pop("quantity_sold", None)
            sale.pop("sold_price", None)
            sale.pop("sold_date", None)
        
        # all expenses
        # all other expenses
        total_expenses = 0
        expenses_details = Expenses.objects.filter(expense_of=id)
        expense_data = get_expense_details(expenses_details)

        for expense in expense_data:
            expense["type"] = "Expenses"
            expense["particular"] = expense["particular"] + " for " + expense["expense_type"]
            expense["quantity"] = str(expense["quantity"]) + " " + expense["unit"]
            expense["duration"] = "-"
            expense["date"] = expense["expense_date"]
            expense["user"] = expense["expense_of"]

            total_expenses += expense["amount"]

            expense.pop("expense_type", None)
            expense.pop("unit", None)
            expense.pop("expense_date", None)
            expense.pop("expense_of", None)

        # all home expenses 
        home_expenses_details = HomeExpenses.objects.filter(expense_of=id)
        home_expenses_data = get_home_expense_details(home_expenses_details)
        
        for home_expense in home_expenses_data:
            home_expense["type"] = "Home Expense"
            home_expense["particular"] = home_expense["product"]["prod_name"] + " " + home_expense["category"]
            home_expense["amount"] = home_expense["estimated_price"]
            home_expense["duration"] = "-"
            home_expense["quantity"] = str(home_expense["quantity"]) + " kg"
            home_expense["user"] = home_expense["expense_of"]

            total_expenses += home_expense["amount"]

            home_expense.pop("category", None)
            home_expense.pop("estimated_price", None)
            home_expense.pop("product", None)
            home_expense.pop("expense_of", None)

        # all bought details
        buy_details = BuyDetails.objects.filter(sold_to=id)
        all_bought_data = get_bought_details(buy_details)
        for bought_equipment in all_bought_data:
            eqp_name = bought_equipment["equipment"]["equipment"]["name"]
            seller_fname = bought_equipment["sold_by"]["first_name"] 
            seller_lname = bought_equipment["sold_by"]["last_name"]

            bought_equipment["type"] = "Bought Detail"
            bought_equipment["particular"] = eqp_name + " from " + seller_fname + " " + seller_lname
            bought_equipment["amount"] = bought_equipment["total_price"]
            bought_equipment["duration"] = "-"
            bought_equipment["date"] = bought_equipment["sold_date"]
            bought_equipment["user"] = bought_equipment["sold_to"]

            total_expenses += bought_equipment["amount"]

            bought_equipment.pop("equipment", None)
            bought_equipment.pop("sold_by", None)
            bought_equipment.pop("total_price", None)
            bought_equipment.pop("sold_date", None)
            bought_equipment.pop("sold_to", None)

        # all rent details
        rent_details = RentDetails.objects.filter(rented_to=id)
        all_rent_data = get_rent_details(rent_details)
        for rented_equipment in all_rent_data:
            eqp_name = rented_equipment["equipment"]["equipment"]["name"]
            seller_fname = rented_equipment["rented_by"]["first_name"] 
            seller_lname = rented_equipment["rented_by"]["last_name"]

            rented_equipment["type"] = "Rent Detail"
            rented_equipment["particular"] = eqp_name + " from " + seller_fname + " " + seller_lname
            rented_equipment["amount"] = rented_equipment["total_price"]
            rented_equipment["duration"] = str(rented_equipment["rented_duration"]) + " hrs."
            rented_equipment["quantity"] = rented_equipment["rented_quantity"]
            rented_equipment["date"] = rented_equipment["rented_date"]
            rented_equipment["user"] = rented_equipment["rented_by"]

            total_expenses += rented_equipment["amount"]

            rented_equipment.pop("equipment", None)
            rented_equipment.pop("rented_to", None)
            rented_equipment.pop("total_price", None)
            rented_equipment.pop("rented_date", None)
            rented_equipment.pop("rented_duration", None)
            rented_equipment.pop("rented_quantity", None)
            rented_equipment.pop("rented_by", None)

        # concatenating all expenses
        all_expenses = expense_data + home_expenses_data + all_bought_data + all_rent_data
        data_to_display = {"Expenses": all_expenses, "Income":product_sold_data, 
                           "TotalIncome": total_income, "TotalExpense": total_expenses, 
                           "NetAmount": total_income - total_expenses}

        return Response(data_to_display)


# modified sold product
class BuyProductRequest(APIView):
    def get(self, request):
        all_products_sold = ProductSold.objects.all()
        products_sold_data = get_sold_details(all_products_sold)
        return Response(products_sold_data)

    def post(self, request):
        serializer = ProductSoldSerializer(data=request.data)
        if serializer.is_valid():
            quantity_requested = float(request.data['quantity_sold'])
            product_requested = request.data["sold_product"]

            product_on_sale = ProductsForSale.objects.filter(id=product_requested)
            if len(product_on_sale) != 0:
                quantity_present = product_on_sale[0].quantity_in_kg
                if quantity_requested < quantity_present:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request": "Not enough quantity present"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRequestDetails(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.get(id=id)
        except ProductSold.DoesNotExist:
            return None

    def get(self, request, id):
        product_sold_detail = self.get_object(id)
        if product_sold_detail != None:
            product_sold = ProductSoldSerializer(product_sold_detail).data
            product_sold_data = modify_sold_data(product_sold)
            return Response(product_sold_data)
        else:
            return Response({})
        

    def put(self, request, id):
        product_sold = self.get_object(id)
        if product_sold != None:
            serializer = ProductSoldSerializer(product_sold, data=request.data)

            if serializer.is_valid():
                requested_quantity = request.data["quantity_sold"]
                current_quantity = product_sold.sold_product.quantity_in_kg
                if not product_sold.seen and not product_sold.approved:
                    if float(requested_quantity) < current_quantity:
                        serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({"Bad Request": "Not enough quantity present"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Bad Request": "The request has been disapproved. You cannot update now."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        product_sold = self.get_object(id)
        if product_sold != None:
            if not product_sold.approved:
                product_sold.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Bad Request": "This request has already been approved. Cannot delete the request now"}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})


class BuyersProductRequests(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.filter(sold_to=id)
        except ProductSold.DoesNotExist:
            return None
    
    def get(self, request, id):
        product_bought = self.get_object(id)
        
        products_bought_data = get_sold_details(product_bought)
        return Response(products_bought_data)
        


class FarmerProductRequests(APIView):
    def get_object(self, id):
        try:
            return ProductSold.objects.filter(sold_product__added_by=id)
        except ProductSold.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        product_sold = self.get_object(id)
        products_sold_data = get_sold_details(product_sold)
        return Response(products_sold_data)


class ChangeProductRequestStatus(APIView):  
    def put(self, request, id):
        product_request = ProductSold.objects.filter(id=id)
        print(product_request)
        if len(product_request) > 0:
            product_id = product_request[0].sold_product.product.id
            farmer_id = product_request[0].sold_product.added_by

            product_stock = ProductStock.objects.filter(product_id=product_id, farmer_id=farmer_id)
            available_stock = product_stock[0].stock

            req_status = request.data["approved"]
            req_seen = product_request[0].seen

            requested_quantity = product_request[0].quantity_sold

            if product_request[0].approved and not req_status:  # handling approved to disapprove request
                qty_to_update = available_stock + requested_quantity
                

            # handling disapprove or yet to see to approve request    
            elif not product_request[0].approved:
                qty_to_update = available_stock - requested_quantity
            
            else:
                qty_to_update = available_stock

            if not req_seen:
                req_seen = True

            
            if qty_to_update>=0: 
                product_stock.update(stock=qty_to_update)
                product_request.update(approved=req_status, seen=req_seen)
                return Response({"success":"Request Status Changed"})
            else:
                return Response({"Bad Request": "Stock Not Available"})
            
        else:
            return Response({})


class ChangeEqpBuyRequestStatus(APIView):  
    def put(self, request, id):
        buy_req = BuyDetails.objects.filter(id=id)
        
        if len(buy_req) > 0:
            req_status = request.data["approved"]
            req_seen = buy_req[0].seen

            if not req_seen:
                req_seen = True
            buy_req.update(approved=req_status, seen=req_seen)
            return Response({"success":"Request Status Changed"})
        else:
            return Response({})


class ChangeEqpRentRequestStatus(APIView):  
    def put(self, request, id):
        rent_req = RentDetails.objects.filter(id=id)
        
        if len(rent_req) > 0:
            req_status = request.data["approved"]
            req_seen = rent_req[0].seen

            if not req_seen:
                req_seen = True
            rent_req.update(approved=req_status, seen=req_seen)
            return Response({"success":"Request Status Changed"})
        else:
            return Response({})


class NPKTestView(APIView):
    def get(self, request):
        npk_test = NPKTest.objects.all()
        serializer = NPKTestSerializer(npk_test, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = NPKTestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NPKTestDetails(APIView):
    def get_object(self, id):
        try:
            return NPKTest.objects.get(id=id)
        except NPKTest.DoesNotExist:
            return None
    
    def get(self, id):
        test = self.get_object(id)
        if test != None:
            serializer = NPKTestSerializer(test)
            return Response(serializer.data)
        else:
            return Response({})
    
    def delete(self, id):
        test = self.get_object(id)
        if test != None:
            test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


class ImageTestView(APIView):
    def get(self, request):
        image_test = ImageTest.objects.all()
        serializer = ImageTestSerializer(image_test, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = NPKTestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageTestDetails(APIView):
    def get_object(self, id):
        try:
            return ImageTest.objects.get(id=id)
        except ImageTest.DoesNotExist:
            return None
    
    def get(self, id):
        test = self.get_object(id)
        if test != None:
            serializer = ImageTestSerializer(test)
            return Response(serializer.data)
        else:
            return Response({})
    
    def delete(self, id):
        test = self.get_object(id)
        if test != None:
            test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})
