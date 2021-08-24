from admins.api.serializers import AvailableUserSerializer
from numpy.core.fromnumeric import product
from farmers.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from vendors.models import *
from farmers.models import *
from rest_framework import status
from farmers.serializers import *
from vendors.serializers import *
from django.db.models import Sum, Q
import os


class DashboardView(APIView):
    def get(self, request):
        # total users count
        farmers_count = Profile.objects.filter(user_type='Farmers').count()
        vendors_count = Profile.objects.filter(user_type='Vendors').count()
        buyers_count = Profile.objects.filter(user_type='Buyers').count()

        prod_categories = {
            "Cereals": 0,
            "Pulses": 0, 
            "Vegetables": 0, 
            "Fruits": 0, 
            "Nuts": 0, 
            "Oilseeds": 0,
            "Sugars and Starches": 0, 
            "Fibres": 0, 
            "Beverages": 0, 
            "Narcotics": 0, 
            "Spices": 0, 
            "Condiments": 0, 
            "Others": 0,
        }

        eqp_categories = {
            "Tractor": 0,
            "Harvester": 0,
            "ATV or UTV": 0,
            "Plows": 0,
            "Harrows": 0,
            "Fertilizer Spreaders": 0,
            "Seeders": 0,
            "Balers": 0,
            "Other": 0,
        }

        all_production = Production.objects.values('product_id__prod_category').annotate(qty=Sum('production_qty')).order_by()
        for production in all_production:
            category = production.get('product_id__prod_category')
            prod_categories[category] = production.get('qty')
                
        products_sold = ProductSold.objects.filter(approved=True
                                                    ).values(
                                                        'sold_product__product__prod_category'
                                                    ).annotate(
                                                        sales=Sum('quantity_sold')
                                                    ).order_by(
                                                        '-sales'
                                                    )[:5]
        prod_sales = []
        for prod_sold in products_sold:
            category = prod_sold.get('sold_product__product__prod_category')
            prod_sales.append({category: prod_sold.get('sales')})
            # prod_categories[category]['sales'] = prod_sold.get('sales')  
        
        equipments_sold = BuyDetails.objects.filter(approved=True
                                                    ).values(
                                                        'equipment__equipment__category'
                                                    ).annotate(
                                                        sales=Sum('quantity')
                                                    ).order_by(
                                                        '-sales'
                                                    )

        eqp_sales = []
        for eqp_sold in equipments_sold[:5]:
            category = eqp_sold.get('equipment__equipment__category')
            eqp_sales.append({category: eqp_sold.get('sales')})
            # eqp_categories[category] = eqp_sold.get('sales')

        for eqp in equipments_sold:
            category = eqp.get('equipment__equipment__category')
            eqp_categories[category] = eqp.get('sales')
        
        data = {
            "total_farmers": farmers_count, 
            "total_vendors": vendors_count, 
            "total_buyers": buyers_count,
            "products": prod_categories,
            'prod_sales': prod_sales,
            'eqp_sales': eqp_sales,
            'equipment': eqp_categories
        }
        return Response(data)




class AvailableUsersView(APIView):
    def get(self, request):
        all_profile = Profile.objects.filter(~Q(user_type='Admins'))
        profile_data = AvailableUserSerializer(all_profile, many=True).data

        for profile in profile_data:
            user_id = profile.get('user')
            user_data = User.objects.get(id=user_id)
            profile["full_name"] = user_data.first_name + " " + user_data.last_name
            profile["is_active"] = user_data.is_active
        return Response(profile_data)


class ActionOnUserView(APIView):
    def put(self, request, user_id):
        user_data = User.objects.filter(id=user_id)
        if len(user_data) > 0:
            is_active = request.data["is_active"]
            user_data.update(is_active=is_active)
            return Response({"Success": "User account disabled"})
        else:
            return Response({"Bad Request": "No Such User Present"})


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
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if product != None:
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        else:
            return Response({})

    def put(self, request, id):
        product = self.get_object(id)

        if product != None:
            serializer = ProductSerializer(product, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        product = self.get_object(id)
        if product != None:
            os.remove(product.prod_img)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({})


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
            return None

    def get(self, request, id):
        equipment = self.get_object(id)
        if equipment != None:
            serializer = EquipmentSerializer(equipment)
            return Response(serializer.data)
        else:
            return Response({})
            
    def put(self, request, id):
        equipment = self.get_object(id)
        if equipment != None:
            serializer = EquipmentSerializer(equipment, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({})

    def delete(self, request, id):
        equipment = self.get_object(id)
        if equipment != None:
            equipment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({})


class FarmersListView(APIView):
    def get(self, request):
        all_farmers = User.objects.filter(profile__user_type='Farmers')
        user_data = []

        for farmer in all_farmers:
            data = {
                "full_name": farmer.first_name + " " + farmer.last_name,
                "address": farmer.profile.address,
                "contact": farmer.profile.contact
            }

            # getting all production
            production_data = Production.objects.filter(farmer_id=farmer.id
                                                        ).values(
                                                            'farmer_id'
                                                        ).annotate(
                                                            qty=Sum('production_qty'),
                                                            area=Sum('area')
                                                        ).order_by()
           
            production_qty = [pd.get('qty') for pd in production_data]                                                 
            farmed_area = [pd.get('area') for pd in production_data]

            # sales
            sales_data = ProductSold.objects.filter(sold_product__added_by=farmer.id, 
                                                    approved=True).values(
                                                        'sold_product__added_by'
                                                    ).annotate(
                                                        sold_qty=Sum('quantity_sold')
                                                    ).order_by()

            sales_qty = [sq.get('sold_qty') for sq in sales_data]

            data["production"] = sum(production_qty)
            data["area"] = sum(farmed_area)
            data["sales"] = sum(sales_qty)

            user_data.append(data)
        return Response(user_data)


class VendorsListView(APIView):
    def get(self, request):
        all_vendors = User.objects.filter(profile__user_type='Vendors')
        user_data = []

        for vendor in all_vendors:
            data = {
                "full_name": vendor.first_name + " " + vendor.last_name,
                "address": vendor.profile.address,
                "contact": vendor.profile.contact
            }

            # sales
            sales_data = BuyDetails.objects.filter(equipment__added_by=vendor.id, 
                                                    approved=True).values(
                                                        'equipment__added_by'
                                                    ).annotate(
                                                        total_price=Sum('total_price')
                                                    ).order_by()

            sales_price = [tp.get('total_price') for tp in sales_data]

            # rents
            rent_data = RentDetails.objects.filter(equipment__added_by=vendor.id, 
                                                    approved=True).values(
                                                        'equipment__added_by'
                                                    ).annotate(
                                                        total_price=Sum('total_price')
                                                    ).order_by()
            rent_price = [tp.get('total_price') for tp in rent_data]  

            data["sales"] = sum(sales_price + rent_price)                                                  

            user_data.append(data)
        return Response(user_data)


class BuyersListView(APIView):
    def get(self, request):
        all_buyers = User.objects.filter(profile__user_type='Buyers')
        user_data = []

        for buyer in all_buyers:
            data = {
                "full_name": buyer.first_name + " " + buyer.last_name,
                "address": buyer.profile.address,
                "contact": buyer.profile.contact
            }

            prod_bought_data = ProductSold.objects.filter(sold_to=buyer.id, 
                                                    approved=True).values(
                                                        'sold_to'
                                                    ).annotate(
                                                        purchase_amt=Sum('sold_price')
                                                    ).order_by()

            prod_purchase_amt = [pa.get('purchase_amt') for pa in prod_bought_data]

            eqp_bought_data = BuyDetails.objects.filter(sold_to=buyer.id,
                                                        approved=True).values(
                                                            'sold_to'
                                                        ).annotate(
                                                            purchase_amt=Sum('total_price')
                                                        ).order_by()
            eqp_bought_amt = [pa.get('purchase_amt') for pa in eqp_bought_data]

            eqp_rented_data = RentDetails.objects.filter(rented_to=buyer.id,
                                                        approved=True).values(
                                                            'rented_to'
                                                        ).annotate(
                                                            purchase_amt=Sum('total_price')
                                                        ).order_by()
            eqp_rented_amt = [pa.get('purchase_amt') for pa in eqp_rented_data] 
            
            total_purchase = sum(prod_purchase_amt + eqp_bought_amt+ eqp_rented_amt)
            data["purchases"] = total_purchase
            
            user_data.append(data)
        return Response(user_data)
