import os
import keras.models
from django.db.models import base
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests.api import head
from accounts.auth import *
from rest_framework.response import Response
from .models import *
from .utils import *
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
# from flask import Flask, request, render_template
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image

# Create your views here.
# base_url = 'http://127.0.0.1:8000'


@login_required
@farmers_only
def index(request):
    return render(request, 'farmers/farmers.html')


@login_required
@farmers_only
def add_product(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        product = data['product']
        quantity_in_kg = data['quantity']
        price_per_kg = data['price']
        details = data['details']
        added_by = request.user.id

        request.data = {
            "product": product,
            "quantity_in_kg": quantity_in_kg,
            "price_per_kg": price_per_kg,
            "added_by": added_by,
            "details": details
        }
        
        product_on_sale_obj = ProductsForSaleView()
        product_on_sale_response = product_on_sale_obj.post(request)
        
        # product_on_sale_endpoint = '/api/productsOnSale/'
        # product_on_sale_url = base_url + product_on_sale_endpoint

        # product_on_sale_response = requests.post(product_on_sale_url, data=product_data, headers=headers)

        if product_on_sale_response.data.get('id') != None:
            print('Product added successfully')
        else:
            error = product_on_sale_response.data
            print(error)

    product_obj = ProductsAPIView()
    product_get_response = product_obj.get(request)
    product_data = product_get_response.data

    # product_get_endpoint = '/api/products/'
    # product_get_url = base_url + product_get_endpoint
    # product_get_response = requests.get(product_get_url, headers=headers)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']

    context = {
        "product": product_data,
        "categories": categories
    }

    return render(request, 'farmers/addProduct.html', context)


@login_required
@farmers_only
def my_products(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    
    # if request.method == 'POST':
    #     comment_post_response = comment_add(request)
    #     if comment_post_response.json().get('id') != None:
    #         print('Comment added successfully')
    #     else:
    #         error = comment_post_response.json()
    #         print(error)
    #         return redirect('/farmers/myProducts')
    
    # calling product api to get all the products added by me
    my_products_obj = MyProductsOnSale()
    product_response = my_products_obj.get(request, user_id=request.user.id)
    
    # product_endpoint = '/api/productsOnSale/mine/' + str(request.user.id)
    # product_url = base_url + product_endpoint
    # product_response = requests.get(product_url, headers=headers)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    
    context = {
        "my_products": product_response.data,
        "categories": categories
    }

    return render(request, 'farmers/myProducts.html', context)


@login_required
@farmers_only
def edit_product(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    product_on_sale_obj = ProductsForSaleDetails()

    if request.method == 'POST':
        data = request.POST
        product = data['product']
        quantity_in_kg = data['quantity']
        price_per_kg = data['price']
        added_by = request.user.id
        details = data['details']

        request.data = {
            "product": product,
            "quantity_in_kg": quantity_in_kg,
            "price_per_kg": price_per_kg,
            "added_by": added_by,
            "details": details
        }
        
        
        product_put_response = product_on_sale_obj.put(request, prod_id)

        # product_put_endpoint = '/api/productsOnSale/' + str(prod_id)
        # product_put_url = base_url + product_put_endpoint

        # product_put_response = requests.put(product_put_url, data=product_put_data, headers=headers)

        if product_put_response.data.get('id') != None:
            print('Product updated successfully')
            return redirect('/farmers/myproducts')
        else:
            error = product_put_response.data
            print(error)
            return redirect('/farmers/editproduct/' + str(prod_id))

    product_details_obj = ProductsAPIView()
    product_details_response = product_details_obj.get(request)
    
    product_get_response = product_on_sale_obj.get(request, prod_id)

    # product_details_endpoint = '/api/products'
    # product_details_url = base_url + product_details_endpoint
    # product_details_response = requests.get(product_details_url, headers=headers)

    # product_get_endpoint = '/api/productsOnSale/' + str(prod_id)
    # product_get_url = base_url + product_get_endpoint
    # product_get_response = requests.get(product_get_url, headers=headers)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    context = {
        'product_detail': product_details_response.data,
        'product': product_get_response.data,
        'categories': categories
    }
    return render(request, 'farmers/editproduct.html', context)



@login_required
@farmers_only
def delete_product(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    product_on_sale_obj = ProductsForSaleDetails()
    product_response = product_on_sale_obj.delete(request, prod_id)

    # product_endpoint = '/api/productsOnSale/' + str(id)
    # product_url = base_url + product_endpoint
    # product_response = requests.delete(product_url, headers=headers)

    if Response(product_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myproducts')


@login_required
@farmers_only
def edit_comment(request, id):
    comment_put_response = comment_edit(request, id)
    if comment_put_response.data.get('id') != None:
        print('Product added successfully')
    else:
        error = comment_put_response.data
        print(error)
    return redirect('/farmers/myproducts')


@login_required
@farmers_only
def delete_comment(request, id):
    comment_del_response = comment_delete(request, id)

    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myproducts')


@login_required
@farmers_only
def add_production(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        product_id = data['product_id']
        farmer_id = request.user.id
        production_qty = data['production_qty']
        area = data['area']

        request.data = {
            "product_id": product_id,
            "farmer_id": farmer_id,
            "production_qty": production_qty,
            "area": area
        }

        production_post_obj = ProductionAPIView()
        production_post_response = production_post_obj.post(request)

        # production_post_endpoint = '/api/products/production/'
        # production_post_url = base_url + production_post_endpoint
        # production_post_response = requests.post(production_post_url, data=production_data, headers=headers)
        if production_post_response.data.get('id') != None:
            print('Production added successfully')
            return redirect('/farmers/addProduction')
        else:
            error = production_post_response.data
            print(error)
            return redirect('/farmers/addProduction')

    product_get_obj = ProductsAPIView()
    product_get_response = product_get_obj.get(request)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    # product_get_endpoint = '/api/products/'
    # product_get_url = base_url + product_get_endpoint
    # product_get_response = requests.get(product_get_url, headers=headers)
    context = {
        "products": product_get_response.data,
        "categories": categories
    }
    return render(request, 'farmers/addProduction.html', context)


@login_required
@farmers_only
def edit_production(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    production_obj = ProductionDetails()
    if request.method == 'POST':
        data = request.POST
        product_id = data['product_id']
        farmer_id = request.user.id
        production_qty = data['production_qty']
        area = data['area']

        request.data = {
            "product_id": product_id,
            "farmer_id": farmer_id,
            "production_qty": production_qty,
            "area": area
        }
        
        production_put_response = production_obj.put(request, id)

        # production_put_endpoint = '/api/products/production/' + str(id)
        # production_put_url = base_url + production_put_endpoint

        # production_put_response = requests.put(production_put_url, data=production_data, headers=headers)
        if production_put_response.data.get('id') != None:
            print('Production updated successfully')
            return redirect('/farmers/myProduction')
        else:
            error = production_put_response.data
            print(error)
            return redirect('/farmers/myProduction')

    production_get_response = production_obj.get(request, id)
    # production_get_endpoint = '/api/products/production/' + str(id)
    # production_get_url = base_url + production_get_endpoint
    # production_get_response = requests.get(production_get_url, headers=headers)

    product_get_obj = ProductsAPIView()
    product_get_response = product_get_obj.get(request)
    # product_get_endpoint = '/api/products/'
    # product_get_url = base_url + product_get_endpoint
    # product_get_response = requests.get(product_get_url, headers=headers)
    context = {
        "production_data": production_get_response.data,
        "products": product_get_response.data,
    }
    return render(request, 'farmers/editProduction.html', context)


@login_required
@farmers_only
def delete_production(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    production_obj = ProductionDetails()
    production_del_response = production_obj.delete(request, id)
    # production_del_endpoint = '/api/products/production/' + str(id)
    # production_del_url = base_url + production_del_endpoint
    # production_del_response = requests.delete(production_del_url, headers=headers)

    if Response(production_del_response).status_code == 200:
        print('Deleted Successfully')

    return redirect('/farmers/myProduction')


# @login_required
# @farmers_only
# def sell_product(request, id):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method == 'POST':
#         data = request.POST
#         sold_product = data["sold_product"]
#         sold_by = request.user.id
#         sold_to = data["sold_to"]
#         quantity_sold = data["quantity_sold"]
#         sold_price = data["sold_price"]
#         remarks = data["remarks"]

#         sold_data = {
#             "sold_product": sold_product,
#             "sold_by": sold_by,
#             "sold_to": sold_to,
#             "quantity_sold": quantity_sold,
#             "sold_price": sold_price,
#             "remarks": remarks,
#         }

#         sell_product_endpoint = '/api/sellProducts/'
#         sell_product_url = base_url + sell_product_endpoint
#         sell_product_response = requests.post(sell_product_url, data=sold_data, headers=headers)

#         if sell_product_response.json().get('id') != None:
#             print('Product sold successfully')
#             return redirect('/farmers/myProducts')
#         else:
#             error = sell_product_response.json()
#             print(error)
#             return redirect('/farmers/myProducts/')

#     product_get_endpoint = '/api/productsOnSale/' + str(id)
#     product_get_url = base_url + product_get_endpoint
#     product_get_response = requests.get(product_get_url, headers=headers)

#     context = {
#         'product_detail': product_get_response.json(),
#     }

#     return render(request, 'farmers/sellProducts.html', context)


# @login_required
# @farmers_only
# def edit_sales(request, id):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method == 'POST':
#         data = request.POST
#         sold_product = data["sold_product"]
#         sold_by = request.user.id
#         sold_to = data["sold_to"]
#         quantity_sold = data["quantity_sold"]
#         sold_price = data["sold_price"]
#         remarks = data["remarks"]

#         sold_data = {
#             "sold_product": sold_product,
#             "sold_by": sold_by,
#             "sold_to": sold_to,
#             "quantity_sold": quantity_sold,
#             "sold_price": sold_price,
#             "remarks": remarks,
#         }

#         edit_sell_product_endpoint = '/api/sellProducts/' + str(id)
#         edit_sell_product_url = base_url + edit_sell_product_endpoint
#         edit_sell_product_response = requests.put(edit_sell_product_url, data=sold_data, headers=headers)

#         if edit_sell_product_response.json().get('id') != None:
#             print('Product sold successfully')
#             return redirect('/farmers/mySales')
#         else:
#             error = edit_sell_product_response.json()
#             print(error)
#             return redirect('/farmers/mySales')

#     sales_get_endpoint = '/api/sellProducts/' + str(id)
#     sales_get_url = base_url + sales_get_endpoint
#     sales_get_response = requests.get(sales_get_url, headers=headers)

#     product_get_endpoint = '/api/productsOnSale/' + str(sales_get_response.json()["sold_product"]["id"])
#     product_get_url = base_url + product_get_endpoint
#     product_get_response = requests.get(product_get_url, headers=headers)

#     context = {
#         "sales_data": sales_get_response.json(),
#         'product_detail': product_get_response.json(),
#     }

#     return render(request, 'farmers/editSales.html', context)


# @login_required
# @farmers_only
# def delete_sales(request, id):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     sales_del_endpoint = '/api/sellProducts/' + str(id)
#     sales_del_url = base_url + sales_del_endpoint
#     sales_del_response = requests.delete(sales_del_url, headers=headers)

#     if Response(sales_del_response).status_code == 200:
#         print('Deleted Successfully')

#     return redirect('/farmers/mySales')


@login_required
@farmers_only
def add_home_expenses(request):

    if request.method == 'POST':
        data = request.POST
        category = data["category"]
        quantity = data["quantity"]
        estimated_price = data["price"]
        remarks = data["remarks"]
        product = data["product"]

        request.data = {
            "category": category,
            "quantity": quantity,
            "estimated_price": estimated_price,
            "remarks": remarks,
            "expense_of": request.user.id,
            "product": product,
        }
        
        home_expense_obj = HomeExpenseAPIView()
        home_expense_response = home_expense_obj.post(request)

        if home_expense_response.data.get('id') != None:
            print('Home Expense added successfully')
        else:
            error = home_expense_response.data
            print(error)
        return redirect('/farmers/addHomeExpenses')

    product_obj = ProductsAPIView()
    product_get_response = product_obj.get(request)
    product_data = product_get_response.data

    prod_categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                        'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                        'Spices', 'Condiments', 'Others']

    expense_type = ["Consumed", "Wastes"]

    context = {
        "product": product_data,
        "prod_categories": prod_categories,
        "expense_type": expense_type
    }

    return render(request, 'farmers/addHomeExpenses.html', context)


@login_required
@farmers_only
def add_expenses(request):
    if request.method == 'POST':
        data = request.POST
        category = data["category"]
        particular = data["particular"]
        unit = data["unit"]
        quantity = data["quantity"]
        amount = data["amount"]
        remarks = data["remarks"]

        request.data = {
            "particular": particular,
            "expense_type": category,
            "unit": unit,
            "quantity": quantity,
            "amount": amount,
            "remarks": remarks,
            "expense_of": request.user.id
        }

        expense_post_obj = ExpenseAPIView()
        expense_post_response = expense_post_obj.post(request)
        if expense_post_response.data.get('id') != None:
            print("Expense added successfully")
        else:
            error = expense_post_response.data
            print(error)
        return redirect('/farmers/addExpenses')

    type_of_expense = [ "Before Harvesting", "During Harvesting", "After Harvesting"]
    context = {
        "type": type_of_expense
    }
    return render(request, 'farmers/addExpenses.html', context)


@login_required
@farmers_only
def my_expenses(request):

    expense_obj = MyExpenses()
    expense_response = expense_obj.get(request, request.user.id)

    context = {
        "my_expense": expense_response.data
    }

    return render(request, 'farmers/Myexpenses.html', context)


@login_required
@farmers_only
def edit_my_expense(request, exp_id):
    expense_obj = ExpenseDetails()

    if request.method == 'POST':
        data = request.POST
        category = data["category"]
        particular = data["particular"]
        unit = data["unit"]
        quantity = data["quantity"]
        amount = data["amount"]
        remarks = data["remarks"]

        request.data = {
            "particular": particular,
            "expense_type": category,
            "unit": unit,
            "quantity": quantity,
            "amount": amount,
            "remarks": remarks,
            "expense_of": request.user.id
        }

        expense_put_response = expense_obj.put(request, exp_id)
        if expense_put_response.data.get('id') != None:
            print("Expense Updated Successfully")
        else:
            error = expense_put_response.data
            print(error)
        return redirect('/farmers/myExpenses')


    type_of_expense = [ "Before Harvesting", "During Harvesting", "After Harvesting"]
    
    expense_response = expense_obj.get(request, exp_id)
    expense_data = ''
    if len(expense_response.data) != 0:
        if expense_response.data["expense_of"]["id"] == request.user.id:
            expense_data = expense_response.data
                

    context = {
        "type": type_of_expense,
        "expense_data": expense_data
    }

    return render(request, 'farmers/editMyExpense.html', context)


@login_required
@farmers_only
def delete_my_expense(request, exp_id):
    expense_obj = ExpenseDetails()
    expense_response = expense_obj.delete(request, exp_id)
    if Response(expense_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myExpenses')


@login_required
@farmers_only
def my_production(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    my_production_obj = MyProductions()
    my_production_response = my_production_obj.get(request, request.user.id)

    # my_production_endpoint = '/api/products/production/mine/' + str(request.user.id)
    # my_production_url = base_url + my_production_endpoint
    # my_production_request = requests.get(my_production_url, headers=headers)
    context = {
        "my_production": my_production_response.data
    }
    return render(request, 'farmers/MyProduction.html', context)


@login_required
@farmers_only
def my_stock(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    my_stock_obj = MyProductStock()
    my_stock_response = my_stock_obj.get(request, request.user.id)

    # my_stock_endpoint = '/api/products/stock/mine/' + str(request.user.id)
    # my_stock_url = base_url + my_stock_endpoint
    # my_stock_request = requests.get(my_stock_url, headers=headers)

    context = {
        "my_stock": my_stock_response.data
    }
    return render(request, 'farmers/Mystock.html', context)


# @login_required
# @farmers_only
# def my_sales(request):
#     headers = {'Authorization': 'Token ' + request.session['token']}

#     product_sales_endpoint = '/api/sellProducts/seller/' + str(request.user.id)
#     product_sales_url = base_url + product_sales_endpoint
#     product_sales_request = requests.get(product_sales_url, headers=headers)
#     context = {
#         "my_sales": product_sales_request.json()
#     }

#     return render(request, 'farmers/Mysales.html', context)





@login_required
@farmers_only
def profit_loss_report(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    report_obj = ProfitLossReportView()
    report_response = report_obj.get(request, request.user.id)
    

    # report_endpoint = '/api/profitloss/' + str(request.user.id)
    # report_url = base_url + report_endpoint
    # report_response = requests.get(report_url, headers=headers).json()
    context = {
        "all_details": report_response.data,
        "net_amount": abs(report_response.data["NetAmount"])
    }

    return render(request, 'farmers/details.html', context)


"""
Soil testing part -----------------------------------------
"""


# @login_required
# @farmers_only
# def test(request):
#     return render(request, 'farmers/Npktest.html')

def getNPK_Prediction(N, P, K, temp, humidity, ph):
    model = pickle.load(open('npk_model.sav', 'rb'))
    scaler = pickle.load(open('scaler.sav', 'rb'))

    prediction = model.predict(scaler.transform([
        [N, P, K, temp, humidity, ph]
    ]))

    crops = {20: 'rice', 11: 'maize', 3: 'chickpea', 9: 'kidneybeans', 18: 'pigeonpeas', 13: 'mothbeans',
             14: 'mungbean', 2: 'blackgram', 10: 'lentil', 19: 'pomegranate', 1: 'banana', 12: 'mango', 7: 'grapes',
             21: 'watermelon', 15: 'muskmelon', 0: 'apple', 16: 'orange', 17: 'papaya', 4: 'coconut', 6: 'cotton',
             8: 'jute', 5: 'coffee'}

    return crops[prediction]


@login_required
@farmers_only
def npk_result(request):
    if request.method == 'POST':
        data = request.POST
        N = int(data['N'])
        P = int(data['P'])
        K = int(data['K'])
        temp = int(data['temp'])
        humidity = int(data['humidity'])
        ph = int(data['ph'])

        
        result = getNPK_Prediction(N, P, K, temp, humidity, ph)
        context = {'result': result}
        return render(request, 'farmers/Npktest.html', context)
    else:
        return render(request, 'farmers/Npktest.html')



# def npk_test(request):
#     return render(request, 'farmers/Npktest.html')

def get_image_model(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    img_model = keras.models.load_model("farmers/model/SoilNet_93_86.h5")
    predict_crops = np.argmax(img_model.predict(image))

    classes = {0: "Alluvial Soil: Rice, Wheat, Sugarcane, Maize, Cotton, Soyabean, Jute",
               1: "Black Soil: Wheat, Jowar, Millet, Linseed, Castor, Sunflower",
               2: "Clay Soil: Rice, Lettuce, Chard, Broccoli, Cabbage, Snap Beans",
               3: "Red Soil: Cotton, Wheat, Pilses, Millet, OilSeeds, Potatoes"}

    prediction = classes[predict_crops]

    return prediction


@login_required
@farmers_only
def image_test(request):
    predict = ''
    if request.method == 'POST':
        image_url = ''
        file = request.FILES['image']
        print(file)
        path = default_storage.save('farmers/model/image_testing/' + str(file), ContentFile(file.read()))
        print(path)

        file_path = os.path.join('', path)
        print(file_path)
        predict = get_image_model(file_path)

    return render(request, 'farmers/imagetest.html', {'img_result': predict})


@login_required
@farmers_only
def general_table(request):
    return render(request, 'farmers/GeneralTable.html')



@login_required
@farmers_only
def profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id)
    # user_detail_endpoint = '/api/users/id/' + str(user_id) + '/details'
    # user_detail_url = base_url + user_detail_endpoint
    # user_detail_response = requests.get(user_detail_url, headers=headers).json()
    context = {
        'user_data': user_detail_response.data
    }
    return render(request, 'farmers/profile.html', context)



@login_required
@farmers_only
def edit_profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id).data
    # user_detail_endpoint = '/api/users/id/' + str(user_id) + '/details'
    # user_detail_url = base_url + user_detail_endpoint
    # user_detail_response = requests.get(user_detail_url, headers=headers).json()

    current_profile_pic = user_detail_response["profile_pic"]

    if request.method == 'POST':
        data = request.POST
        username = request.user.username
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        user = user_id
        bio = data["bio"]
        contact = data["contact"]
        address = data["address"]

        try:
            profile_pic = request.FILES["profile_pic"]
        except:
            profile_pic = None

        image_path = current_profile_pic
        if not profile_pic == None:
            try:
                Image.open(profile_pic)
                image_path = default_storage.save('static/profile_pic/' + str(profile_pic), profile_pic)
            except:
                print("Not Valid Image")
                return redirect('/farmers/profile/' + str(user_id) + '/edit')
        
        request.data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "user": user,
            "bio": bio,
            "contact": contact,
            "address": address,
            "profile_pic": image_path,
        }
        # print(data_to_update)
        update_profile_obj = UpdateProfileView()
        user_put_response = update_profile_obj.put(request, user_id)
        # user_put_endpoint = '/api/profile/' + str(user_id) +'/edit'
        # user_put_url = base_url + user_put_endpoint
        # user_put_response = requests.put(user_put_url, data=data_to_update, headers=headers)
        if user_put_response.data.get('username') != None:
            print('Profile updated successfully')
            return redirect('/farmers/profile/' + str(user_id))
        else:
            error = user_put_response.data
            print(error)
        return redirect('/farmers/profile/' + str(user_id) + '/edit')

    context = {
        'user_data': user_detail_response
    }
    return render(request, 'farmers/editProfile.html', context)


@login_required
@farmers_only
def all_equipments(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    eqp_display_obj = EquipmentsToDisplayView()
    all_equipment_response = eqp_display_obj.get(request)
    # all_equipment_endpoint = '/api/equipmentToDisplay/'
    # all_equipment_url = base_url + all_equipment_endpoint
    # all_equipment_response = requests.get(all_equipment_url, headers=headers).json()
    context = {
        "all_equipments": all_equipment_response.data,
    }

    return render(request, 'farmers/allEquipments.html', context)



@login_required
@farmers_only
def equipment_details(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        comment = data['comment']
        equipment = eqp_id
        comment_by = request.user.id

        request.data = {
            "comment_by": comment_by,
            "equipment": equipment,
            "comment": comment
        }

        comment_post_obj = EquipmentCommentView()
        comment_post_response = comment_post_obj.post(request)
        
        # comment_post_endpoint = '/api/equipmentToDisplay/comments'
        # comment_post_url = base_url + comment_post_endpoint
        # comment_post_response = requests.post(comment_post_url, headers=headers, data=comment_post_data)

        if comment_post_response.data.get('id') != None:
            print('Comment submitted successfully')
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))
        else:
            error = comment_post_response.data
            print(error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))

    equipment_detail_obj = EquipmentsToDisplayDetails()
    equipment_detail_response = equipment_detail_obj.get(request, eqp_id)
    # equipment_detail_endpoint = '/api/equipmentToDisplay/' + str(eqp_id)
    # equipment_detail_url = base_url + equipment_detail_endpoint
    # equipment_detail_response = requests.get(equipment_detail_url, headers=headers).data
    context = {
        "equipment_detail": equipment_detail_response.data,
    }
    return render(request, 'farmers/equipmentDetails.html', context)



@login_required
@farmers_only
def purchase_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        equipment_detail_obj = EquipmentsToDisplayDetails()
        equipment_detail_response = equipment_detail_obj.get(request, eqp_id).data
        # equipment_detail_endpoint = '/api/equipmentToDisplay/' + str(eqp_id)
        # equipment_detail_url = base_url + equipment_detail_endpoint
        # equipment_detail_response = requests.get(equipment_detail_url, headers=headers).json()
        price_per_item = equipment_detail_response["price_to_buy_per_item"]

        data = request.POST
        equipment = eqp_id
        sold_to = request.user.id
        quantity = data["quantity"]
        delivered_address = data['address']
        total_price = int(price_per_item) * int(quantity)
        remarks = data['remarks']

        request.data = {
            "equipment": equipment,
            "sold_to": sold_to,
            "quantity": quantity,
            "delivered_address": delivered_address,
            "total_price": total_price,
            "remarks": remarks,
        }
        
        buy_equipment_obj = BuyEquipmentView()
        buy_equipment_response = buy_equipment_obj.post(request)
        # buy_equipment_endpoint = '/api/equipmentToDisplay/buy'
        # buy_equipment_url = base_url + buy_equipment_endpoint
        # buy_equipment_response = requests.post(buy_equipment_url, data=buy_data, headers=headers)

        if buy_equipment_response.data.get('id') != None:
            print('Request submitted successfully')
            return redirect('/farmers/allEquipments/')
        else:
            error = buy_equipment_response.data
            print(error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))

    return redirect('/farmers/equipmentdetails/' + str(eqp_id))


@login_required
@farmers_only
def rent_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        equipment_detail_obj = EquipmentsToDisplayDetails()
        equipment_detail_response = equipment_detail_obj.get(request, eqp_id).data
        # equipment_detail_endpoint = '/api/equipmentToDisplay/' + str(eqp_id)
        # equipment_detail_url = base_url + equipment_detail_endpoint
        # equipment_detail_response = requests.get(equipment_detail_url, headers=headers).json()
        price_per_hour = equipment_detail_response["price_per_hour"]

        data = request.POST
        equipment = eqp_id
        rented_to = request.user.id
        rented_quantity = data["quantity"]

        day = data["day"]
        hours = data["hours"]
        delivered_address = data['address']
        rented_duration = (int(day) * 24) + int(hours)
        total_price = rented_duration * int(rented_quantity) * int(price_per_hour)

        remarks = data['remarks']

        request.data = {
            "equipment": equipment,
            "rented_to": rented_to,
            "rented_quantity": rented_quantity,
            "delivered_address": delivered_address,
            "rented_duration": rented_duration,
            "total_price": total_price,
            "remarks": remarks,
        }
        
        rent_equipment_obj = RentEquipmentView()
        rent_equipment_response = rent_equipment_obj.post(request)
        # rent_equipment_endpoint = '/api/equipmentToDisplay/rent'
        # rent_equipment_url = base_url + rent_equipment_endpoint
        # rent_equipment_response = requests.post(rent_equipment_url, data=rent_data, headers=headers)

        if rent_equipment_response.data.get('id') != None:
            print('Request submitted successfully')
            return redirect('/farmers/allEquipments/')
        else:
            error = rent_equipment_response.data
            print(error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))
    return redirect('/farmers/equipmentdetails/' + str(eqp_id))

# @login_required
# @farmers_only
# def edit_product(request):
#     return render(request, 'farmers/editProduct.html')
# def add_product(request):
#     return render(request, 'farmers/addProduct.html')

@login_required
@farmers_only
def product_details(request, prod_id):
    if request.method == 'POST':
        comment_post_response = comment_add(request, prod_id)
        if comment_post_response.data.get('id') != None:
            print("Comment Added Successfully")
        else:
            error = comment_post_response.data
            print(error)
        return redirect('/farmers/myproducts/' + str(prod_id))

    product_details_obj = ProductsForSaleDetails()
    product_details_response = product_details_obj.get(request, prod_id)
    context = {
        "product_data": product_details_response.data
    }


    return render(request, 'farmers/productDetails.html', context)
