from django.shortcuts import render
from accounts.auth import *
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response

# Create your views here.
base_url = 'http://127.0.0.1:8000'

@login_required
@admin_only
def index(request):
    return render(request, 'admins/admins.html')



@login_required
@admin_only
def add_products(request):
    categories = ["Cereals", "Pulses", "Vegetables", "Fruits", "Nuts", "Oilseeds",
                  "Sugars and Starches", "Fibres", "Beverages", "Narcotics", "Spices", 
                  "Condiments", "Others"]
    context = {
        "categories": categories
    }
    if request.method == 'POST':
        data = request.POST
        prod_name = data['name']
        prod_category = data['category']
        # prod_img = request.FILES["image"]
        

        product_data = {
            "prod_name": prod_name,
            "prod_category": prod_category,
            # "prod_img": prod_img,
        }
        
        product_endpoint = '/api/products/'
        product_url = base_url + product_endpoint
        headers = {'Authorization': 'Token ' + request.session['token']}

        product_response = requests.post(product_url, data=product_data, headers=headers)
        # print(product_response.json().get('id'))
        if product_response.json().get('id') != None:
            print('Product added successfully')
        else:
            error = product_response.json()
            print(error)
     
    return render(request, 'admins/addProducts.html', context)