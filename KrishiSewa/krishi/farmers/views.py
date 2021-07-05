from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
from rest_framework.response import Response
from .models import *
from .utils import *



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
            print('Product added successfully')
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
        prod_name = data['name']
        quantity_in_kg = data['quantity']
        prod_category = data['category']
        prod_price = data['price']
        # prod_img = data['image']
        prod_added_by = request.user.id

        product_post_data = {
            "prod_name": prod_name,
            "quantity_in_kg": float(quantity_in_kg),
            "prod_category": prod_category,
            "prod_price": float(prod_price),
            # "prod_img": prod_img,
            "prod_added_by": prod_added_by
        }
        

        product_post_endpoint = '/api/products/'+str(id)
        product_post_url = base_url + product_post_endpoint

        product_post_response = requests.put(product_post_url, data=product_post_data, headers=headers)
        if Response(product_post_response).status_code == 200:

            print('Product updated successfully')
            return redirect('/farmers/myProducts')


    product_get_endpoint = '/api/products/' + str(id)
    product_get_url = base_url + product_get_endpoint
    product_get_response = requests.get(product_get_url, headers=headers)
    if Response(product_get_response).status_code == 200:
        product_get_data = product_get_response.json()

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    context = {
        'product': product_get_data,
        'categories': categories
    }
    return render(request, 'farmers/editProducts.html', context)


@login_required
@farmers_only
def delete_product(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    product_endpoint = '/api/products/' + str(id)
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
def result(request):
    N = int(request.GET['N'])
    P = int(request.GET['P'])
    K = int(request.GET['K'])
    temp = int(request.GET['temp'])
    humidity = int(request.GET['humidity'])
    ph = int(request.GET['ph'])

    result = getNPK_Prediction(N, P, K, temp, humidity, ph)

    return render(request, 'farmers/npk_result.html', {'result': result})


@login_required
@farmers_only
def image_test(request):
    return render(request, 'farmers/imagetest.html')
