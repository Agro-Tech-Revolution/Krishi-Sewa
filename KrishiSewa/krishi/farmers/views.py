
import os
import keras.models
from django.db.models import base
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
from rest_framework.response import Response
from .models import *
from .utils import *
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from flask import Flask, request, render_template



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
            "quantity_in_kg": float(quantity_in_kg),
            "price_per_kg": float(price_per_kg),
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
            "quantity_in_kg": float(quantity_in_kg),
            "price_per_kg": float(price_per_kg),
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
"""
Soil testing part -----------------------------------------
"""


@login_required
@farmers_only
def test(request):
    return render(request, 'farmers/index.html')


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
def result(request):
    N = int(request.GET['N'])
    P = int(request.GET['P'])
    K = int(request.GET['K'])
    temp = int(request.GET['temp'])
    humidity = int(request.GET['humidity'])
    ph = int(request.GET['ph'])

    result = getNPK_Prediction(N, P, K, temp, humidity, ph)

    return render(request, 'farmers/npk_result.html', {'result': result})


def get_image_model(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    img_model = keras.models.load_model("SoilNet_93_86.h5")
    predict_crops = np.argmax(img_model.predict(image))

    classes = {0: "Alluvial Soil:-{ Rice,Wheat,Sugarcane,Maize,Cotton,Soyabean,Jute }",
               1: "Black Soil:-{ Virginia, Wheat , Jowar,Millets,Linseed,Castor,Sunflower} ",
               2: "Clay Soil:-{ Rice,Lettuce,Chard,Broccoli,Cabbage,Snap Beans }",
               3: "Red Soil:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }"}

    prediction = classes[predict_crops]

    return prediction


def imageTest(request):
    if request.method == 'POST':
        file = request.files['image']  # fet input
        filename = file.filename
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
        crop_predict = get_image_model(file_path)

        return redirect(request, {'result': crop_predict})

@login_required
@farmers_only
def image_test(request):
    return render(request, 'farmers/imagetest.html')

