from re import T
from vendors.serializers import BuyDetailsSerializer, EquipmentCommentSerializer, EquipmentReportSerializer, EquipmentSerializer, EquipmentToDisplaySerializer, RentDetailsSerializer
from vendors.models import Equipment, EquipmentComment, EquipmentReport, EquipmentToDisplay
from farmers.serializers import *
from .serializers import *

def modify_product_details_data(product):
    prod_id = product['id']

    product_details = Products.objects.get(id=product['product'])
    product_details_data = ProductSerializer(product_details).data

    user_details = User.objects.get(id=product['added_by'])
    user_details_data = UserSerializer(user_details).data

    profile_details = Profile.objects.get(user=product['added_by'])
    profile_details_data = UpdateProfileSerializer(profile_details).data
    user_details_data["profile"] = profile_details_data

    comments_details = ProductComment.objects.filter(product=prod_id)
    comments_data = ProductCommentSerializer(comments_details, many=True).data

    for comment in comments_data:
        user_comment_details = User.objects.get(id=comment['comment_by'])
        user_comment_data = UserSerializer(user_comment_details).data

        comment_profile_details = Profile.objects.get(user=comment['comment_by'])
        comment_profile_details_data = UpdateProfileSerializer(comment_profile_details).data
        user_comment_data["profile"] = comment_profile_details_data

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


def modify_equipment_detail_data(equipment):
    eqp_id = equipment['id']

    equipment_details = Equipment.objects.get(id=equipment['equipment'])
    equipment_details_data = EquipmentSerializer(equipment_details).data

    user_details = User.objects.get(id=equipment['added_by'])
    user_details_data = UserSerializer(user_details).data

    profile_details = Profile.objects.get(user=equipment['added_by'])
    profile_details_data = UpdateProfileSerializer(profile_details).data
    user_details_data["profile"] = profile_details_data

    reports_details = EquipmentReport.objects.filter(reported_equipment=eqp_id)
    report_data = EquipmentReportSerializer(reports_details, many=True).data

    for report in report_data:
        user_report_details = User.objects.get(id=report['reported_by'])
        user_report_data = UserSerializer(user_report_details).data
        report['reported_by'] = user_report_data
    
    comment_details = EquipmentComment.objects.filter(equipment=eqp_id)
    comment_data = EquipmentCommentSerializer(comment_details, many=True).data

    for comment in comment_data:
        user_comment_details = User.objects.get(id=comment['comment_by'])
        user_comment_data = UserSerializer(user_comment_details).data

        comment_profile_details = Profile.objects.get(user=comment['comment_by'])
        comment_profile_details_data = UpdateProfileSerializer(comment_profile_details).data
        user_comment_data["profile"] = comment_profile_details_data

        comment['comment_by'] = user_comment_data


    equipment['equipment'] = equipment_details_data
    equipment['added_by'] = user_details_data
    equipment['reports'] = report_data
    equipment['comments'] = comment_data

    return equipment


def get_equipment_details(equipment_to_display):
    equipment_data = EquipmentToDisplaySerializer(equipment_to_display, many=True).data

    for equipment in equipment_data:
        
        equipment = modify_equipment_detail_data(equipment)
    return equipment_data


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

    product_id = stock_data["product_id"]["id"]
    farmer_id = stock_data["farmer_id"]["id"]

    # total production
    production_detail = Production.objects.filter(product_id=product_id, farmer_id=farmer_id)
    total_produciton_qty = 0
    for production_data in production_detail:
        total_produciton_qty += production_data.production_qty
    stock_data["total_production"] = total_produciton_qty

    # total sales
    sold_product_detail = ProductSold.objects.filter(sold_product__product__id=product_id, sold_product__added_by=farmer_id, approved=True)
    total_sales = 0
    for sale in sold_product_detail:
        total_sales += sale.quantity_sold
    stock_data["total_sales"] = total_sales

    # total home expense
    home_expense_detail = HomeExpenses.objects.filter(product__id=product_id, expense_of=farmer_id)
    total_home_expense = 0
    for expense in home_expense_detail:
        total_home_expense += expense.quantity
    stock_data["total_expense"] = total_home_expense

    return stock_data


def get_product_stock_data(product_stock):
    product_stock_data = ProductStockSerializer(product_stock, many=True).data
    for stock_data in product_stock_data:
        stock_data = modify_product_stock_data(stock_data)
    return product_stock_data


def modify_sold_data(sold_products):
    product_for_sale_details = ProductsForSale.objects.get(id=sold_products['sold_product'])
    product_for_sale_data = SerialzerForSold(product_for_sale_details).data # this is from ProductsForSale

    product_details = Products.objects.get(id=product_for_sale_data['product'])
    product_details_data = ProductSerializer(product_details).data  # this is from Products
    product_for_sale_data['product'] = product_details_data
    sold_products['sold_product'] = product_for_sale_data
    
    farmer_details = User.objects.get(id=sold_products['sold_product']['added_by'])
    farmer_data = UserSerializer(farmer_details).data

    buyer_details = User.objects.get(id=sold_products['sold_to'])
    buyer_data = UserSerializer(buyer_details).data

    profile_details = Profile.objects.get(user=buyer_data['id'])
    profile_details_data = UpdateProfileSerializer(profile_details).data
    buyer_data["profile"] = profile_details_data

    
    sold_products['sold_by'] = farmer_data
    sold_products['sold_to'] = buyer_data
    return sold_products


def get_sold_details(all_products_sold):
    products_sold_data = ProductSoldSerializer(all_products_sold, many=True).data
    for sold_products in products_sold_data:
        sold_products = modify_sold_data(sold_products)
    return products_sold_data


def modify_bought_data(bought_equipment):
    equipment_to_buy_details = EquipmentToDisplay.objects.get(id=bought_equipment['equipment'])
    equipment_to_buy_data = EquipmentToDisplaySerializer(equipment_to_buy_details).data 

    equipment_details = Equipment.objects.get(id=equipment_to_buy_data['equipment'])
    equipment_details_data = EquipmentSerializer(equipment_details).data
    equipment_to_buy_data['equipment'] = equipment_details_data
    bought_equipment['equipment'] = equipment_to_buy_data  
    
    vendor_details = User.objects.get(id=bought_equipment['equipment']['added_by'])
    vendor_data = UserSerializer(vendor_details).data

    buyer_details = User.objects.get(id=bought_equipment['sold_to'])
    buyer_data = UserSerializer(buyer_details).data

    profile_details = Profile.objects.get(user=buyer_data['id'])
    profile_details_data = UpdateProfileSerializer(profile_details).data
    buyer_data["profile"] = profile_details_data

    bought_equipment['sold_by'] = vendor_data
    bought_equipment['sold_to'] = buyer_data
    return bought_equipment


def get_bought_details(all_bought_data):
    equipment_bought_data = BuyDetailsSerializer(all_bought_data, many=True).data
    for equipment_bought in equipment_bought_data:
        equipment_bought = modify_bought_data(equipment_bought)
    return equipment_bought_data


def modify_rented_data(equipment_rented):
    equipment_to_rent_details = EquipmentToDisplay.objects.get(id=equipment_rented['equipment'])
    equipment_to_rent_data = EquipmentToDisplaySerializer(equipment_to_rent_details).data 

    equipment_details = Equipment.objects.get(id=equipment_to_rent_data['equipment'])
    equipment_details_data = EquipmentSerializer(equipment_details).data
    equipment_to_rent_data['equipment'] = equipment_details_data
    equipment_rented['equipment'] = equipment_to_rent_data  
    
    vendor_details = User.objects.get(id=equipment_rented['equipment']['added_by'])
    vendor_data = UserSerializer(vendor_details).data

    buyer_details = User.objects.get(id=equipment_rented['rented_to'])
    buyer_data = UserSerializer(buyer_details).data
    
    profile_details = Profile.objects.get(user=buyer_data['id'])
    profile_details_data = UpdateProfileSerializer(profile_details).data
    buyer_data["profile"] = profile_details_data

    equipment_rented['rented_by'] = vendor_data
    equipment_rented['rented_to'] = buyer_data
    return equipment_rented


def get_rent_details(all_rent_data):
    equipment_rented_data = RentDetailsSerializer(all_rent_data, many=True).data
    for equipment_rented in equipment_rented_data:
        equipment_rented = modify_rented_data(equipment_rented)
    return equipment_rented_data


def modify_expense_details(expense):
    user_details = User.objects.get(id=expense['expense_of'])
    user_details_data = UserSerializer(user_details).data
    expense['expense_of'] = user_details_data
    return expense


def get_expense_details(all_expense_data):
    expense_data = ExpenseSerializer(all_expense_data, many=True).data
    for expense in expense_data:
        expense = modify_expense_details(expense)
    
    return expense_data


def modify_home_expense_data(expense_data):
    user_details = User.objects.get(id=expense_data['expense_of'])
    user_details_data = UserSerializer(user_details).data
    expense_data['expense_of'] = user_details_data

    product_details = Products.objects.get(id=expense_data['product'])
    product_details_data = ProductSerializer(product_details).data
    expense_data['product'] = product_details_data
    return expense_data


def get_home_expense_details(all_home_expense_data):
    home_expense_data = HomeExpenseSerializer(all_home_expense_data, many=True).data
    for expense in home_expense_data:
        expense = modify_home_expense_data(expense)

    return home_expense_data