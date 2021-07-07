from farmers.serializers import *
from .serializers import *

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

    product_id = stock_data["product_id"]["id"]
    farmer_id = stock_data["farmer_id"]["id"]

    # total production
    production_detail = Production.objects.filter(product_id=product_id, farmer_id=farmer_id)
    total_produciton_qty = 0
    for production_data in production_detail:
        total_produciton_qty += production_data.production_qty
    stock_data["total_production"] = total_produciton_qty

    # total sales
    sold_product_detail = ProductSold.objects.filter(sold_product__product__id=product_id, sold_by=farmer_id)
    total_sales = 0
    for sale in sold_product_detail:
        total_sales += sale.quantity_sold
    stock_data["total_sales"] = total_sales

    
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
