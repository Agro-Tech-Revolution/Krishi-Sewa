from django.db.models import base
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests.api import head
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
def products(request):
    
    if request.method == 'POST':
        data = request.POST
        prod_name = data['name']
        quantity_in_kg = data['quantity']
        prod_category = data['category']
        prod_price = data['price']
        prod_added_by = request.user.id

        product_data = {
            "prod_name": prod_name,
            "quantity_in_kg": float(quantity_in_kg),
            "prod_category": prod_category,
            "prod_price": float(prod_price),
            "prod_added_by": prod_added_by
        }

        product_endpoint = '/api/products/'
        product_url = base_url + product_endpoint
        headers = {'Authorization': 'Token ' + request.session['token']}

        product_response = requests.post(product_url, data=product_data, headers=headers)
        if Response(product_response).status_code == 200:

            print('Product added successfully. Product id is: ' + str(product_response.json().get('id')))
        
    return render(request, 'farmers/addProducts.html')


@login_required
@farmers_only
def my_products(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    if request.method=='POST':
        comment_post_response = comment_add(request)
        if Response(comment_post_response).status_code == 200:
            print('Comment Added Successfully')
            return redirect('/farmers/myProducts')

    # calling product api to get all the products added by me
    product_endpoint = '/api/products/mine/' + str(request.user.id)
    product_url = base_url + product_endpoint
    product_response = requests.get(product_url, headers=headers)

    products_by_me = []
    if Response(product_response).status_code == 200:
        products_by_me = product_response.json()
        
    # calling comment api to get all the comments of products added by logged in user
    comment_endpoint = '/api/products/comments/user/' + str(request.user.id)
    comment_url = base_url + comment_endpoint
    comment_response = requests.get(comment_url, headers=headers)

    comments_on_my_products = []
    if Response(comment_response).status_code == 200:
        comments_on_my_products = comment_response.json()

    # modifiying comments keys and values so that the name of the person who commmented can be seen
    for comment in comments_on_my_products:
        user_endpoint = '/api/users/id/'+str(comment['comment_by'])
        user_url = base_url + user_endpoint
        user_response = requests.get(user_url, headers=headers)
        if Response(user_response).status_code == 200:
            comment['comment_by'] = user_response.json()

    # appending comments of a product to products dictionary
    for products in products_by_me:
        comments_for_a_product = []
        for comment in comments_on_my_products:
            if comment['product'] == products['id']:
                comments_for_a_product.append(comment)
        products['comments'] = comments_for_a_product
        
    context = {
        "my_products": products_by_me,
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
        prod_added_by = request.user.id

        product_post_data = {
            "prod_name": prod_name,
            "quantity_in_kg": float(quantity_in_kg),
            "prod_category": prod_category,
            "prod_price": float(prod_price),
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
    
    if Response(comment_put_response).status_code == 200:
        print('Comment Updated Successfully')
    return redirect('/farmers/myProducts')


@login_required
@farmers_only
def delete_comment(request, id):
    comment_del_response = comment_delete(request, id)
    
    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/farmers/myProducts')