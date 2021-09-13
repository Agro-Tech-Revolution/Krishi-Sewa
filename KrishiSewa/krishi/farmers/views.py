import os
import keras.models
from django.db.models import base
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from numpy.core.fromnumeric import product
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
from PIL import Image
from django.core.files.base import ContentFile
from admins.api.views import *
from django.contrib import messages

# Create your views here.
# base_url = 'http://127.0.0.1:8000'


@login_required
@farmers_only
def index(request):
    return render(request, 'farmers/farmers.html')


@login_required
@farmers_only
def feedback(request):
    return render(request, 'farmers/user-feedback.html')


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

        if product_on_sale_response.data.get('id') != None:
            messages.success(request, "Product added successfully")
        else:
            error = product_on_sale_response.data
            messages.error(request, error)

    product_obj = ProductsAPIView()
    product_get_response = product_obj.get(request)
    product_data = product_get_response.data


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

    
    # calling product api to get all the products added by me
    my_products_obj = MyProductsOnSale()
    product_response = my_products_obj.get(request, user_id=request.user.id)
    product_data = product_response.data

    if request.method == 'POST':
        product_data = search_prod(request)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
    
    context = {
        "my_products": product_data,
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

        if product_put_response.data.get('id') != None:
            messages.success(request, "Product updated successfully")
            return redirect('/farmers/myproducts')
        else:
            error = product_put_response.data
            messages.error(request, error)
            return redirect('/farmers/editproduct/' + str(prod_id))

    product_details_obj = ProductsAPIView()
    product_details_response = product_details_obj.get(request)
    
    product_get_response = product_on_sale_obj.get(request, prod_id)

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

    if Response(product_response).status_code == 200:
        messages.success(request, "Deleted successfully")
    return redirect('/farmers/myproducts')


@login_required
@farmers_only
def edit_comment(request, id):
    comment_put_response = comment_edit(request, id)
    if comment_put_response.data.get('id') != None:
        messages.success(request, "Comment updated successfully")
    else:
        error = comment_put_response.data
        messages.error(request, error)
    return redirect('/farmers/myproducts')


@login_required
@farmers_only
def delete_comment(request, id):
    comment_del_response = comment_delete(request, id)

    if Response(comment_del_response).status_code == 200:
        messages.success(request, "Comment deleted successfully")
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

        if production_post_response.data.get('id') != None:
            messages.success(request, "Production added successfully")
            return redirect('/farmers/addProduction')
        else:
            error = production_post_response.data
            messages.error(request, error)
            return redirect('/farmers/addProduction')

    product_get_obj = ProductsAPIView()
    product_get_response = product_get_obj.get(request)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']
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

        if production_put_response.data.get('id') != None:
            messages.success(request, "Production updated successfully")

            return redirect('/farmers/myProduction')
        else:
            error = production_put_response.data
            messages.error(request, error)
            return redirect('/farmers/myProduction')

    production_get_response = production_obj.get(request, id)

    product_get_obj = ProductsAPIView()
    product_get_response = product_get_obj.get(request)

    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']

    context = {
        "production_data": production_get_response.data,
        "products": product_get_response.data,
        "categories": categories
    }
    return render(request, 'farmers/editProduction.html', context)


@login_required
@farmers_only
def delete_production(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    production_obj = ProductionDetails()
    production_del_response = production_obj.delete(request, id)

    if Response(production_del_response).status_code == 200:
        messages.success(request, "Deleted successfully")

    return redirect('/farmers/myProduction')


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
            messages.success(request, "Home expense added successfully")
        else:
            error = home_expense_response.data
            messages.error(request, error)
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
def my_home_expenses(request):
    home_expense_obj = MyHomeExpense()
    home_expense_response = home_expense_obj.get(request, request.user.id)
    context = {
        "my_home_expense": home_expense_response.data
    }
    return render(request, 'farmers/MyHomeExpenses.html', context)

@login_required
@farmers_only
def edit_home_expense(request, exp_id):
    home_expense_obj = HomeExpenseDetails()
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

        home_expense_put_response = home_expense_obj.put(request, exp_id)

        if home_expense_put_response.data.get('id') != None:
            messages.success(request, "Home expense updated successfully")
            return redirect('/farmers/myHomeExpenses')
        else:
            error = home_expense_put_response.data
            messages.error(request, error)
            return redirect('/farmers/editHomeExpense/' + str(exp_id))

    product_obj = ProductsAPIView()
    product_get_response = product_obj.get(request)
    product_data = product_get_response.data

    prod_categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                        'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                        'Spices', 'Condiments', 'Others']

    expense_type = ["Consumed", "Wastes"]


    home_expense_response = home_expense_obj.get(request, exp_id)
    
    context = {
        "product": product_data,
        "prod_categories": prod_categories,
        "expense_type": expense_type,
        "expense_data": home_expense_response.data
    }

    return render(request, 'farmers/editHomeExpense.html', context)


@login_required
@farmers_only
def delete_home_expense(request, exp_id):
    home_expense_obj = HomeExpenseDetails()
    home_expense_response = home_expense_obj.delete(request, exp_id)
    if Response(home_expense_response).status_code == 200:
        messages.success(request, "Deleted successfully")
    return redirect('/farmers/myHomeExpenses')


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
            messages.success(request, "Expense added successfully")
        else:
            error = expense_post_response.data
            messages.error(request, error)
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
            messages.success(request, "Expense updated successfully")

        else:
            error = expense_put_response.data
            messages.error(request, error)
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
        messages.success(request, "Deleted successfully")
    return redirect('/farmers/myExpenses')


@login_required
@farmers_only
def my_production(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    my_production_obj = MyProductions()
    my_production_response = my_production_obj.get(request, request.user.id)

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

    context = {
        "my_stock": my_stock_response.data
    }
    return render(request, 'farmers/Mystock.html', context)


@login_required
@farmers_only
def my_sales(request):

    product_request_obj = FarmerProductRequests()
    product_request_response = product_request_obj.get(request, request.user.id)
    all_data = product_request_response.data

    product_request = [prod_req for prod_req in all_data if prod_req["approved"]]
    
    context = {
        "my_sales": product_request
    }
    return render(request, 'farmers/Mysales.html', context)


@login_required
@farmers_only
def profit_loss_report(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    report_obj = ProfitLossReportView()
    report_response = report_obj.get(request, request.user.id)
    
    context = {
        "all_details": report_response.data,
        "net_amount": abs(report_response.data["NetAmount"])
    }

    return render(request, 'farmers/profit_loss.html', context)


"""
Soil testing part -----------------------------------------
"""
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
    return crops[prediction[0]]


@login_required
@farmers_only
def npk_result(request):
    if request.method == 'POST':
        data = request.POST
        N = data['N']
        P = data['P']
        K = data['K']
        temp = data['temp']
        humidity = data['humidity']
        ph = data['ph']

        result = getNPK_Prediction(int(N), int(P), int(K), int(temp), int(humidity), int(ph))
        context = {'result': result}

        request.data = {
            "nitrogen": N,
            "phosphorus": P,
            "potassium": K,
            "temperature": temp,
            "humidity": humidity,
            "ph": ph,
            "reccommended_crop": result,
            "test_of": request.user.id
        }
        npk_test_obj = NPKTestView()
        npk_test_response = npk_test_obj.post(request)
        if npk_test_response.data.get('id') != None:
            messages.success(request, "Success")
        else:
            error = npk_test_response.data
            messages.error(request, error)
        return render(request, 'farmers/Npktest.html', context)
    else:
        return render(request, 'farmers/Npktest.html')

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
        try:
            image = request.FILES["image"]
        except:
            image = None

        image_path = ''
        if not image == None:
            try:
                Image.open(image)
                image_path = default_storage.save('static/image_test/' + str(image), image)
            except:
                messages.error(request, "Not valid image")
                return redirect('/farmers/imagetest')

        file_path = os.path.join('', image_path)
        predict = get_image_model(file_path)
        request.data = {
            "image": file_path,
            "reccomended_crops": predict,
            "test_of": request.user.id
        }
        image_test_obj = ImageTestView()
        image_test_response = image_test_obj.post(request)
        if image_test_response.data.get('id') != None:
            messages.success(request, "Success")
        else:
            error = image_test_response.data
            messages.error(request, error)

    return render(request, 'farmers/imagetest.html', {'img_result': predict})

@login_required
@farmers_only
def npk_records(request):
    npk_obj = NPKTestView()
    npk_data = npk_obj.get(request).data
    context = {
        'npk_records': npk_data
    }
    return render(request, 'farmers/npk_test_records.html', context)

@login_required
@farmers_only
def image_test_records(request):
    img_test_obj = ImageTestView()
    img_test_data = img_test_obj.get(request).data
    context = {
        'img_test_records': img_test_data
    }
    return render(request, 'farmers/image_test_records.html', context)


@login_required
@farmers_only
def profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id)

    user_report_data = user_detail_response.data.get('reports') 
    reported = False
    for report in user_report_data:
        if report["reported_by"] == request.user.id:
            reported = True
            break

    report_category = ["False Information", "Fake Account", "Posts Disturbing content", "Something Else"]
    context = {
        'user_data': user_detail_response.data,
        'report_category': report_category,
        'reported': reported
    }
    return render(request, 'farmers/profile.html', context)



@login_required
@farmers_only
def edit_profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id).data

    current_profile_pic = user_detail_response["profile_pic"]

    if request.method == 'POST':
        user_put_response = update_profile_data(request, user_id, current_profile_pic)
        if user_put_response.data.get('username') != None:
            messages.success(request, "Profile updated successfully")
            return redirect('/farmers/profile/' + str(user_id))
        else:
            error = user_put_response.data
            messages.error(request, error)
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
    eqp_data = all_equipment_response.data

    if request.method == 'POST':
        eqp_data = search_eqp(request)

    eqp_reported = []
    for eqp in eqp_data:
        for eqp_reports in eqp["reports"]:
            if eqp_reports["reported_by"]["id"] == request.user.id:
                eqp_reported.append(eqp)
    
    for eqp in eqp_reported:
        eqp_data.remove(eqp)

    context = {
        "all_equipments": eqp_data,
        "user_type": "farmers",
    }

    return render(request, 'farmers/allEquipments.html', context)



@login_required
@farmers_only
def equipment_details(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        comment_post_response = comment_add_eqp(request, eqp_id)

        if comment_post_response.data.get('id') != None:
            messages.success(request, "Comment submitted successfully")
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))
        else:
            error = comment_post_response.data
            messages.error(request, error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))

    equipment_detail_obj = EquipmentsToDisplayDetails()
    equipment_detail_response = equipment_detail_obj.get(request, eqp_id)

    report_category = ["False Information", "Fake Equipments", "Misinformation",  "Something Else"]
    if len(equipment_detail_response.data) > 0:
        eqp_report_data = equipment_detail_response.data.get('reports') 
        reported = False
        for report in eqp_report_data:
            if report["reported_by"]["id"] == request.user.id:
                reported = True
                break
    else:
        reported = True

    context = {
        "equipment_detail": equipment_detail_response.data,
        "report_category": report_category,
        "reported": reported
    }
    return render(request, 'farmers/equipmentDetails.html', context)


@login_required
@farmers_only
def report_eqp_view(request, eqp_id):
    if request.method == 'POST':
        eqp_report_response = report_eqp(request, eqp_id)
        if eqp_report_response.data.get('id') != 'None':
            messages.success(request, "Reported successfully")
        else:
            messages.error(request, eqp_report_response.data)
            return redirect('/farmers/equipmentDetails/'+str(eqp_id))

    return redirect('/farmers/allEquipments/')


@login_required
@farmers_only
def purchase_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        buy_equipment_response = purchase_eqp_request(request, eqp_id)

        if buy_equipment_response.data.get('id') != None:
            messages.success(request, "Request submitted successfully")
            return redirect('/farmers/allEquipments/')
        else:
            error = buy_equipment_response.data
            messages.error(request, error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))

    return redirect('/farmers/equipmentdetails/' + str(eqp_id))


@login_required
@farmers_only
def rent_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        rent_equipment_response = rent_eqp_request(request, eqp_id)
        
        if rent_equipment_response.data.get('id') != None:
            messages.success(request, "Request submitted successfully")
            return redirect('/farmers/allEquipments/')
        else:
            error = rent_equipment_response.data
            messages.error(request, error)
            return redirect('/farmers/equipmentdetails/' + str(eqp_id))
    return redirect('/farmers/equipmentdetails/' + str(eqp_id))


@login_required
@farmers_only
def product_details(request, prod_id):
    if request.method == 'POST':
        comment_post_response = comment_add(request, prod_id)
        if comment_post_response.data.get('id') != None:
            messages.success(request, "Comment added successfully")
        else:
            error = comment_post_response.data
            messages.error(request, error)
        return redirect('/farmers/myproducts/' + str(prod_id))

    product_details_obj = ProductsForSaleDetails()
    product_details_response = product_details_obj.get(request, prod_id)
    context = {
        "product_data": product_details_response.data
    }
    return render(request, 'farmers/productDetails.html', context)


@login_required
@farmers_only
def product_requests(request, action=None):
    product_request_obj = FarmerProductRequests()
    product_request_response = product_request_obj.get(request, request.user.id)
    all_data = product_request_response.data

    product_request = []
    seen = ""
    approved = ""
    if action == None:
        product_request = [prod_req for prod_req in all_data if not prod_req["approved"] and not prod_req["seen"]]
        seen = False
        approved = False
    elif action == 'approved':
        product_request = [prod_req for prod_req in all_data if prod_req["approved"]]
        seen = True
        approved = True
    elif action == 'disapproved':
        product_request = [prod_req for prod_req in all_data if not prod_req["approved"] and prod_req["seen"]]
        seen = True
        approved = False

    context = {
        "product_request": product_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'farmers/productRequests.html', context)

@login_required
@farmers_only
def approve_product_request(request, prod_req_id):
    request.data = {
        "approved": True
    }
    prod_req_obj = ChangeProductRequestStatus()
    prod_req_response = prod_req_obj.put(request, prod_req_id)
    if prod_req_response.data.get("success") != None:
        messages.success(request, prod_req_response.data)
    else:
        messages.error(request, prod_req_response.data)
    return redirect('/farmers/productRequests')


@login_required
@farmers_only
def disapprove_product_request(request, prod_req_id):
    request.data = {
        "approved": False
    }
    prod_req_obj = ChangeProductRequestStatus()
    prod_req_response = prod_req_obj.put(request, prod_req_id)
    if prod_req_response.data.get("success") != None:
        messages.success(request, prod_req_response.data)
    else:
        messages.error(request, "Error")
    return redirect('/farmers/productRequests')


@login_required
@farmers_only
def equipment_bought_requests(request, action=None):
    eqp_request, seen, approved = buy_eqp_req(request, action)

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'farmers/eqpBoughtRequests.html', context)


@login_required
@farmers_only
def equipment_rented_requests(request, action=None):
    eqp_request, seen, approved = rent_eqp_req(request, action)

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'farmers/eqpRentRequests.html', context)


@login_required
@farmers_only
def approved_eqp_requests(request, action): 
    eqp_request, table = eqp_approved(request, action)

    context = {
        "eqp_request": eqp_request,
        "table": table
    }

    return render(request, 'farmers/eqpApproved.html', context)


@login_required
@farmers_only
def edit_eqp_buy_requests(request, req_id):
    eqp_req_obj = BuyEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)

    if request.method == 'POST':
        eqp_req_put_response = edit_eqp_buy(request, req_id)

        if eqp_req_put_response.data.get('id') != None:
            messages.success(request, "Updated successfully")
        else:
            messages.error(request, eqp_req_put_response.data)
        return redirect("/farmers/eqpBuyRequests")

    eqp_req_data = ""
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["sold_to"]["id"] == request.user.id:
            eqp_req_data = eqp_req_response.data
        
    context = {
        "eqp_req_data": eqp_req_data
    }
    return render(request, "farmers/editEqpBuyRequest.html", context)


@login_required
@farmers_only
def delete_eqp_buy_requests(request, req_id):
    eqp_req_obj = BuyEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["sold_to"]["id"] == request.user.id:
            eqp_req_del_response = eqp_req_obj.delete(request, req_id)
            if Response(eqp_req_del_response).status_code == 200:
                messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "Sorry cannot perform the request")
    return redirect('/farmers/eqpBuyRequests')


@login_required
@farmers_only
def edit_eqp_rent_requests(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if request.method == 'POST':
        eqp_req_put_response = edit_eqp_rent(request, req_id)
        if eqp_req_put_response.data.get('id') != None:
            messages.success(request, "Updated successfully")
        else:
            messages.error(request, eqp_req_put_response.data)
        return redirect("/farmers/eqpRentRequests")

    eqp_req_data = ""
    hours = ""
    day = ""
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["rented_to"]["id"] == request.user.id:
            eqp_req_data = eqp_req_response.data
            total_duration = eqp_req_data["rented_duration"]
            if total_duration >= 24:
                day = total_duration//24
                hours = total_duration - (day*24)
            else:
                hours = total_duration

    context = {
        "eqp_req_data": eqp_req_data,
        "hours": hours,
        "day": day
    }
    return render(request, "farmers/editEqpRentRequest.html", context)


@login_required
@farmers_only
def delete_eqp_rent_requests(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["rented_to"]["id"] == request.user.id:
            eqp_req_del_response = eqp_req_obj.delete(request, req_id)
            if Response(eqp_req_del_response).status_code == 200:
                messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "Sorry cannot perform the request")
    return redirect('/farmers/eqpRentRequests')


@login_required
@farmers_only
def view_ticket(request):
    my_ticket_obj = MyTickets()
    my_ticket_data = my_ticket_obj.get(request, request.user.id).data
    
    context = {
        "all_tickets": my_ticket_data
    }
    return render(request, 'farmers/viewTicket.html', context)

@login_required
@farmers_only
def change_password(request):
    return render(request, 'farmers/changePassword.html')


