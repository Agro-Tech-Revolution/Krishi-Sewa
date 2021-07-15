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
from flask import Flask, request, render_template
from django.core.files.storage import  default_storage
from django.core.files.base import ContentFile
from django.conf import settings



# Create your views here.
base_url = 'http://127.0.0.1:8000'


@login_required
@farmers_only
def index(request):
    return render(request, 'farmers/farmers.html')


@login_required
@farmers_only
def products_for_sale(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        product = data['product']
        quantity_in_kg = data['quantity']
        price_per_kg = data['price']
        added_by = request.user.id

        product_data = {
            "product": product,
            "quantity_in_kg": quantity_in_kg,
            "price_per_kg": price_per_kg,
            "added_by": added_by
        }
        
        product_on_sale_endpoint = '/api/productsOnSale/'
        product_on_sale_url = base_url + product_on_sale_endpoint
        
        product_on_sale_response = requests.post(product_on_sale_url, data=product_data, headers=headers)
        if product_on_sale_response.json().get('id') != None:
            print('Product added successfully')
        else:
            error = product_on_sale_response.json()
            print(error)

    product_get_endpoint = '/api/products/'
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)
    context = {
        "products": product_get_response.json()
    }

    return render(request, 'farmers/productsForSale.html', context)


@login_required
@farmers_only
def my_products(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    if request.method=='POST':
        comment_post_response = comment_add(request)
        if comment_post_response.json().get('id') != None:
            print('Comment added successfully')
        else:
            error = comment_post_response.json()
            print(error)
            return redirect('/farmers/myProducts')

    # calling product api to get all the products added by me
    product_endpoint = '/api/productsOnSale/mine/' + str(request.user.id)
    product_url = base_url + product_endpoint
    product_response = requests.get(product_url, headers=headers)  
        
    context = {
        "my_products": product_response.json(),
    }    

    return render(request, 'farmers/myProducts.html', context)


@login_required
@farmers_only
def edit_products(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    if request.method == 'POST':
        data = request.POST
        product = data['product']
        quantity_in_kg = data['quantity']
        price_per_kg = data['price']
        added_by = request.user.id

        product_put_data = {
            "product": product,
            "quantity_in_kg": quantity_in_kg,
            "price_per_kg": price_per_kg,
            "added_by": added_by
        }

        product_put_endpoint = '/api/productsOnSale/'+str(id)
        product_put_url = base_url + product_put_endpoint

        product_put_response = requests.put(product_put_url, data=product_put_data, headers=headers)
        if product_put_response.json().get('id') != None:
            print('Product updated successfully')
            return redirect('/farmers/myProducts')
        else:
            error = product_put_response.json()
            print(error)
            return redirect('/farmers/myProducts')
    
    product_details_endpoint = '/api/products'
    product_details_url = base_url + product_details_endpoint
    product_details_response = requests.get(product_details_url, headers=headers)

    product_get_endpoint = '/api/productsOnSale/' + str(id)
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    context = {
        'product_detail': product_details_response.json(),
        'product': product_get_response.json(),
        'categories': categories
    }
    return render(request, 'farmers/editProducts.html', context)


@login_required
@farmers_only
def delete_product(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    product_endpoint = '/api/productsOnSale/' + str(id)
    product_url = base_url + product_endpoint
    product_response = requests.delete(product_url, headers=headers)

    if Response(product_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myProducts')


@login_required
@farmers_only
def edit_comment(request):
    
    comment_put_response = comment_edit(request)
    if comment_put_response.json().get('id') != None:
        print('Product added successfully')
    else:
        error = comment_put_response.json()
        print(error)
    return redirect('/farmers/myProducts')


@login_required
@farmers_only
def delete_comment(request, id):
    comment_del_response = comment_delete(request, id)
    
    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myProducts')


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

        production_data = {
            "product_id": product_id,
            "farmer_id": farmer_id,
            "production_qty": production_qty,
            "area": area
        }

        production_post_endpoint = '/api/products/production/'
        production_post_url = base_url + production_post_endpoint

        production_post_response = requests.post(production_post_url, data=production_data, headers=headers)
        if production_post_response.json().get('id') != None:
            print('Product added successfully')
            return redirect('/farmers/addProduction')
        else:
            error = production_post_response.json()
            print(error)
            return redirect('/farmers/addProduction')


    product_get_endpoint = '/api/products/'
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)
    context = {
        "products": product_get_response.json()
    }
    return render(request, 'farmers/addProduction.html', context)


@login_required
@farmers_only
def edit_production(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    
    if request.method == 'POST':
        data = request.POST
        product_id = data['product_id']
        farmer_id = request.user.id
        production_qty = data['production_qty']
        area = data['area']

        production_data = {
            "product_id": product_id,
            "farmer_id": farmer_id,
            "production_qty": production_qty,
            "area": area
        }

        production_put_endpoint = '/api/products/production/' + str(id)
        production_put_url = base_url + production_put_endpoint

        production_put_response = requests.put(production_put_url, data=production_data, headers=headers)
        if production_put_response.json().get('id') != None:
            print('Product updated successfully')
            return redirect('/farmers/myProduction')
        else:
            error = production_put_response.json()
            print(error)
            return redirect('/farmers/myProduction')


    production_get_endpoint = '/api/products/production/' + str(id)
    production_get_url = base_url + production_get_endpoint
    production_get_response = requests.get(production_get_url, headers=headers)

    product_get_endpoint = '/api/products/'
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)
    context = {
        "production_data": production_get_response.json(),
        "products": product_get_response.json(),
    }
    return render(request, 'farmers/editProduction.html', context)


@login_required
@farmers_only
def delete_production(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    production_del_endpoint = '/api/products/production/' + str(id)
    production_del_url = base_url + production_del_endpoint
    production_del_response = requests.delete(production_del_url, headers=headers)

    if Response(production_del_response).status_code == 200:
        print('Deleted Successfully')
    
    return redirect('/farmers/myProduction')


@login_required
@farmers_only
def sell_product(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        sold_product = data["sold_product"]
        sold_by = request.user.id
        sold_to = data["sold_to"]
        quantity_sold = data["quantity_sold"]
        sold_price = data["sold_price"]
        remarks = data["remarks"]

        sold_data = {
            "sold_product": sold_product,
            "sold_by": sold_by,
            "sold_to": sold_to,
            "quantity_sold": quantity_sold,
            "sold_price": sold_price,
            "remarks": remarks,
        }

        sell_product_endpoint = '/api/sellProducts/'
        sell_product_url = base_url + sell_product_endpoint
        sell_product_response = requests.post(sell_product_url, data=sold_data, headers=headers)

        if sell_product_response.json().get('id') != None:
            print('Product sold successfully')
            return redirect('/farmers/myProducts')
        else:
            error = sell_product_response.json()
            print(error)
            return redirect('/farmers/myProducts/')

    product_get_endpoint = '/api/productsOnSale/' + str(id)
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)

    context = {
        'product_detail': product_get_response.json(),
    }

    return render(request,'farmers/sellProducts.html', context)


@login_required
@farmers_only
def edit_sales(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        sold_product = data["sold_product"]
        sold_by = request.user.id
        sold_to = data["sold_to"]
        quantity_sold = data["quantity_sold"]
        sold_price = data["sold_price"]
        remarks = data["remarks"]

        sold_data = {
            "sold_product": sold_product,
            "sold_by": sold_by,
            "sold_to": sold_to,
            "quantity_sold": quantity_sold,
            "sold_price": sold_price,
            "remarks": remarks,
        }

        edit_sell_product_endpoint = '/api/sellProducts/' + str(id)
        edit_sell_product_url = base_url + edit_sell_product_endpoint
        edit_sell_product_response = requests.put(edit_sell_product_url, data=sold_data, headers=headers)

        if edit_sell_product_response.json().get('id') != None:
            print('Product sold successfully')
            return redirect('/farmers/mySales')
        else:
            error = edit_sell_product_response.json()
            print(error)
            return redirect('/farmers/mySales')

    sales_get_endpoint = '/api/sellProducts/' + str(id)
    sales_get_url = base_url + sales_get_endpoint
    sales_get_response = requests.get(sales_get_url, headers=headers)

    product_get_endpoint = '/api/productsOnSale/' + str(sales_get_response.json()["sold_product"]["id"])
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers) 

    context = {
        "sales_data": sales_get_response.json(),
        'product_detail': product_get_response.json(),
    }


    return render(request, 'farmers/editSales.html', context)


@login_required
@farmers_only
def delete_sales(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    sales_del_endpoint = '/api/sellProducts/' + str(id)
    sales_del_url = base_url + sales_del_endpoint
    sales_del_response = requests.delete(sales_del_url, headers=headers)

    if Response(sales_del_response).status_code == 200:
        print('Deleted Successfully')
    
    return redirect('/farmers/mySales')


@login_required
@farmers_only
def add_expenses(request):
    return render(request,'farmers/addExpenses.html')


@login_required
@farmers_only
def my_production(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    my_production_endpoint = '/api/products/production/mine/' + str(request.user.id)
    my_production_url = base_url + my_production_endpoint
    my_production_request = requests.get(my_production_url, headers=headers)
    context = {
        "my_production": my_production_request.json()
    }
    return render(request, 'farmers/MyProduction.html', context)


@login_required
@farmers_only
def my_stock(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    my_stock_endpoint = '/api/products/stock/mine/' + str(request.user.id)
    my_stock_url = base_url + my_stock_endpoint
    my_stock_request = requests.get(my_stock_url, headers=headers)
    context = {
        "my_stock": my_stock_request.json()
    }
    return render(request, 'farmers/Mystock.html', context)


@login_required
@farmers_only
def my_sales(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    product_sales_endpoint = '/api/sellProducts/seller/' + str(request.user.id)
    product_sales_url = base_url + product_sales_endpoint
    product_sales_request = requests.get(product_sales_url, headers=headers)
    context = {
        "my_sales": product_sales_request.json()
    }

    return render(request, 'farmers/Mysales.html', context)


@login_required
@farmers_only
def my_expenses(request):
    return render(request, 'farmers/Myexpenses.html')


"""
Soil testing part -----------------------------------------
"""


# @login_required
# @farmers_only
# def test(request):
#     return render(request, 'farmers/Npktest.html')


@login_required
@farmers_only
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

        print(N)
        result = getNPK_Prediction(N, P, K, temp, humidity, ph)
        context = {'result': result}
        return render(request, 'farmers/Npktest.html', context)
    else:
        return render(request, 'farmers/Npktest.html')



@login_required
@farmers_only
def image_test(request):
    return render(request, 'farmers/imagetest.html')


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
               1: "Black Soil: Virginia, Wheat, Jowar, Millet, Linseed, Castor, Sunflower",
               2: "Clay Soil: Rice, Lettuce, Chard, Broccoli, Cabbage, Snap Beans",
               3: "Red Soil: Cotton, Wheat, Pilses, Millet, OilSeeds, Potatoes"}

    prediction = classes[predict_crops]

    return prediction


def image_test1(request):
    predict=''
    if request.method =='POST':
        image_url = ''
        file = request.FILES['image']
        print(file)
        path = default_storage.save('farmers/model/image_testing/'+str(file), ContentFile(file.read()))
        print(path)

        file_path = os.path.join('', path)
        print(file_path)
        predict = get_image_model(file_path)

    return render(request, 'farmers/imagetest.html', { 'img_result': predict })

# @login_required
# @farmers_only
# def image_test(request):
#     return render(request, 'farmers/imagetest.html')


