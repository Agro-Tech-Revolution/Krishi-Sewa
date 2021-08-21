from django.shortcuts import render
from accounts.auth import *
from django.contrib.auth.decorators import login_required
from farmers.utils import *
from vendors.utils import *

# Create your views here.
@login_required
@buyers_only
def index(request):
    return render(request, 'buyers/buyers.html')

@login_required
@buyers_only
def report_form(request):
    return render(request, 'buyers/ReportForm.html')


# @login_required
# @buyers_only
# def view_products(request):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method=='POST':
#         comment_post_response = comment_add(request)
#         if Response(comment_post_response).status_code == 200:
#             print('Comment Added Successfully')
#             return redirect('/buyers/viewProducts')
    
#     product_endpoint = '/api/products/' 
#     product_url = base_url + product_endpoint
#     product_response = requests.get(product_url, headers=headers)

#     all_products = []
#     if Response(product_response).status_code == 200:
#         all_products = product_response.json()


#     report_categories = ["False Information", "Fake Products", "Misinformation", "Something Else"]
    
#     context = {
#         "all_products": all_products,
#         "report_categories": report_categories
#     } 

#     return render(request, 'buyers/allProducts.html', context)


# @login_required
# @buyers_only
# def edit_comment(request):
#     comment_put_response = comment_edit(request)
    
#     if Response(comment_put_response).status_code == 200:
#         print('Comment Updated Successfully')
#     return redirect('/buyers/viewProducts')


# @login_required
# @buyers_only
# def delete_comment(request, id):
#     comment_del_response = comment_delete(request, id)
    
#     if Response(comment_del_response).status_code == 200:
#         print('Deleted Successfully')
#     return redirect('/buyers/viewProducts')


# @login_required
# @buyers_only
# def report_product(request):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method == 'POST':
#         data = request.POST
#         reported_product = data['prod_id']
#         report_category = data['category']
#         report_description = data['description']
#         reported_by = request.user.id

#         request.data = {
#             "reported_by": reported_by,
#             "reported_product": reported_product,
#             "report_category": report_category,
#             "report_description": report_description
#         }

#         report_obj = ProductReportView()
#         report_response = report_obj.post(request)
#         # report_endpoint = '/api/products/reports'
#         # report_url = base_url + report_endpoint
#         # report_response = requests.post(report_url, data=report_data, headers=headers)
#         if Response(report_response).status_code == 200:
#             print("Product Reported Successfully")
#         return redirect('/buyers/viewProducts')


# products start
@login_required
@buyers_only
def all_products(request):
    prod_display_obj = ProductsForSaleView()
    all_product_response = prod_display_obj.get(request)

    context = {
        "all_products": all_product_response.data,
        "user_type": 'buyers',
    }

    return render(request, 'buyers/allProducts.html', context)


@login_required
@buyers_only
def product_details(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        comment_post_response = comment_add(request, prod_id)

        if comment_post_response.data.get('id') != None:
            print('Comment submitted successfully')
            return redirect('/buyers/productdetails/' + str(prod_id))
        else:
            error = comment_post_response.data
            print(error)
            return redirect('/buyers/productdetails/' + str(prod_id))

    product_detail_obj = ProductsForSaleDetails()
    product_detail_response = product_detail_obj.get(request, prod_id)
    context = {
        "product_detail": product_detail_response.data,
    }
    return render(request, 'buyers/productDetails.html', context)


@login_required
@buyers_only
def buy_product_request(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        product_detail_obj = ProductsForSaleDetails()
        product_detail_response = product_detail_obj.get(request, prod_id).data
        price_per_kg = product_detail_response["price_per_kg"]

        data = request.POST
        sold_product = prod_id
        sold_to = request.user.id
        quantity_sold = data["quantity"]
        sold_price = int(price_per_kg) * int(quantity_sold)
        remarks = data['remarks']

        request.data = {
            "sold_product": sold_product,
            "sold_to": sold_to,
            "quantity_sold": quantity_sold,
            "sold_price": sold_price,
            "remarks": remarks,
        }
        
        buy_product_obj = BuyProductRequest()
        buy_product_response = buy_product_obj.post(request)

        if buy_product_response.data.get('id') != None:
            print('Request submitted successfully')
            return redirect('/buyers/allProducts/')
        else:
            error = buy_product_response.data
            print(error)
            return redirect('/buyers/productdetails/' + str(prod_id))

    return redirect('/buyers/productdetails/' + str(prod_id))


@login_required
@buyers_only
def product_bought_requests(request, action=None):
    prod_request_obj = BuyersProductRequests()
    product_request_response = prod_request_obj.get(request, request.user.id)
    all_data = product_request_response.data
    
    prod_request = []
    seen = ""
    approved = ""
    if action == None:
        prod_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and not eqp_req["seen"]]
        seen = False
        approved = False
    elif action == 'approved':
        prod_request = [eqp_req for eqp_req in all_data if eqp_req["approved"]]
        seen = True
        approved = True
    elif action == 'disapproved':
        prod_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and eqp_req["seen"]]
        seen = True
        approved = False

    context = {
        "prod_request": prod_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'buyers/prodBoughtRequests.html', context)


@login_required
@buyers_only
def approved_prod_requests(request): 
    product_request_response = ""

    prod_request_obj = BuyersProductRequests()
    product_request_response = prod_request_obj.get(request, request.user.id).data
     
    all_data = product_request_response
    prod_request = [prod_req for prod_req in all_data if prod_req["approved"]]

    context = {
        "prod_request": prod_request,
    }

    return render(request, 'buyers/prodApproved.html', context)


@login_required
@buyers_only
def edit_prod_buy_requests(request, req_id):
    prod_req_obj = ProductRequestDetails()
    prod_req_response = prod_req_obj.get(request, req_id)

    if request.method == 'POST':
        data = request.POST
        quantity_sold = data["quantity"]
        remarks = data["remarks"]
        sold_price = float(quantity_sold) * prod_req_response.data["sold_product"]["price_per_kg"]
        request.data = {
            "quantity_sold": quantity_sold,
            "remarks": remarks,
            "sold_price": sold_price,
        }
        
        prod_req_put_response = prod_req_obj.put(request, req_id)

        if prod_req_put_response.data.get('id') != None:
            print("Updated Successfully")
        else:
            print(prod_req_put_response.data)
        return redirect("/buyers/prodBuyRequests")

    prod_req_data = ""
    if len(prod_req_response.data) > 0:
        if prod_req_response.data["sold_to"]["id"] == request.user.id:
            prod_req_data = prod_req_response.data
        
    context = {
        "prod_req_data": prod_req_data
    }
    return render(request, "buyers/editProdBuyRequest.html", context)


@login_required
@buyers_only
def delete_prod_buy_requests(request, req_id):
    prod_req_obj = ProductRequestDetails()
    prod_req_response = prod_req_obj.get(request, req_id)
    
    if len(prod_req_response.data) > 0:
        if prod_req_response.data["sold_to"]["id"] == request.user.id:
            prod_req_del_response = prod_req_obj.delete(request, req_id)
            if Response(prod_req_del_response).status_code == 200:
                print('Deleted Successfully')
    else:
        print("Sorry Cannot perform the request")
    return redirect('/buyers/prodBuyRequests')



# equipments start
@login_required
@buyers_only
def all_equipments(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    eqp_display_obj = EquipmentsToDisplayView()
    all_equipment_response = eqp_display_obj.get(request)

    context = {
        "all_equipments": all_equipment_response.data,
        "user_type": 'buyers',
    }

    return render(request, 'buyers/allEquipments.html', context)


@login_required
@buyers_only
def equipment_details(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        comment_post_response = comment_add_eqp(request, eqp_id)

        if comment_post_response.data.get('id') != None:
            print('Comment submitted successfully')
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))
        else:
            error = comment_post_response.data
            print(error)
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))

    equipment_detail_obj = EquipmentsToDisplayDetails()
    equipment_detail_response = equipment_detail_obj.get(request, eqp_id)
    context = {
        "equipment_detail": equipment_detail_response.data,
    }
    return render(request, 'buyers/equipmentDetails.html', context)


@login_required
@buyers_only
def purchase_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        buy_equipment_response = purchase_eqp_request(request, eqp_id)

        if buy_equipment_response.data.get('id') != None:
            print('Request submitted successfully')
            return redirect('/buyers/allEquipments/')
        else:
            error = buy_equipment_response.data
            print(error)
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))

    return redirect('/buyers/equipmentdetails/' + str(eqp_id))


@login_required
@buyers_only
def rent_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        rent_equipment_response = rent_eqp_request(request, eqp_id)
        
        if rent_equipment_response.data.get('id') != None:
            print('Request submitted successfully')
            return redirect('/buyers/allEquipments/')
        else:
            error = rent_equipment_response.data
            print(error)
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))
    return redirect('/buyers/equipmentdetails/' + str(eqp_id))


@login_required
@buyers_only
def equipment_bought_requests(request, action=None):
    eqp_request, seen, approved = buy_eqp_req(request, action)

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'buyers/eqpBoughtRequests.html', context)


@login_required
@buyers_only
def equipment_rented_requests(request, action=None):
    eqp_request, seen, approved = rent_eqp_req(request, action)

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'buyers/eqpRentRequests.html', context)


@login_required
@buyers_only
def approved_eqp_requests(request, action): 
    eqp_request, table = eqp_approved(request, action)

    context = {
        "eqp_request": eqp_request,
        "table": table
    }

    return render(request, 'buyers/eqpApproved.html', context)


@login_required
@buyers_only
def edit_eqp_buy_requests(request, req_id):
    eqp_req_obj = BuyEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)

    if request.method == 'POST':
        eqp_req_put_response = edit_eqp_buy(request, req_id)

        if eqp_req_put_response.data.get('id') != None:
            print("Updated Successfully")
        else:
            print(eqp_req_put_response.data)
        return redirect("/buyers/eqpBuyRequests")

    eqp_req_data = ""
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["sold_to"]["id"] == request.user.id:
            eqp_req_data = eqp_req_response.data
        
    context = {
        "eqp_req_data": eqp_req_data
    }
    return render(request, "buyers/editEqpBuyRequest.html", context)


@login_required
@buyers_only
def delete_eqp_buy_requests(request, req_id):
    eqp_req_obj = BuyEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["sold_to"]["id"] == request.user.id:
            eqp_req_del_response = eqp_req_obj.delete(request, req_id)
            if Response(eqp_req_del_response).status_code == 200:
                print('Deleted Successfully')
    else:
        print("Sorry Cannot perform the request")
    return redirect('/buyers/eqpBuyRequests')


@login_required
@buyers_only
def edit_eqp_rent_requests(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if request.method == 'POST':
        eqp_req_put_response = edit_eqp_rent(request, req_id)
        if eqp_req_put_response.data.get('id') != None:
            print("Updated Successfully")
        else:
            print(eqp_req_put_response.data)
        return redirect("/buyers/eqpRentRequests")

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
    return render(request, "buyers/editEqpRentRequest.html", context)


@login_required
@buyers_only
def delete_eqp_rent_requests(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if len(eqp_req_response.data) > 0:
        if eqp_req_response.data["rented_to"]["id"] == request.user.id:
            eqp_req_del_response = eqp_req_obj.delete(request, req_id)
            if Response(eqp_req_del_response).status_code == 200:
                print('Deleted Successfully')
    else:
        print("Sorry Cannot perform the request")
    return redirect('/buyers/eqpRentRequests')





# @login_required
# @buyers_only
# def view_equipments(request):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method=='POST':
#         comment_post_response = eqp_comment_add(request)
#         if Response(comment_post_response).status_code == 200:
#             print('Comment Added Successfully')
#             return redirect('/buyers/viewEquipments')
    
#     equipment_get_endpoint = '/api/equipment/' 
#     equipmet_get_url = base_url + equipment_get_endpoint
#     equipment_get_response = requests.get(equipmet_get_url, headers=headers)

#     all_equipments = []
#     if Response(equipment_get_response).status_code == 200:
#         all_equipments = equipment_get_response.json()

#     # calling comment api to get all the comments 
#     comment_endpoint = '/api/equipment/comments'
#     comment_url = base_url + comment_endpoint
#     comment_response = requests.get(comment_url, headers=headers)

#     all_comments = []
#     if Response(comment_response).status_code == 200:
#         all_comments = comment_response.json()

#     # modifiying comments keys and values so that the name of the person who commmented can be seen
#     for comment in all_comments:
#         user_endpoint = '/api/users/id/'+str(comment['comment_by'])
#         user_url = base_url + user_endpoint
#         user_response = requests.get(user_url, headers=headers)
#         if Response(user_response).status_code == 200:
#             comment['comment_by'] = user_response.json()
    
#     # appending comments of a equipment to equipments dictionary
#     for equipment in all_equipments:
#         comments_for_a_equipment = []
#         for comment in all_comments:
#             if comment['equipment'] == equipment['id']:
#                 comments_for_a_equipment.append(comment)
#         equipment['comments'] = comments_for_a_equipment

#     # calling report api to find all the equipments that the logged in user has reported
#     report_endpoint = '/api/equipment/reports/users/' + str(request.user.id)
#     report_url = base_url + report_endpoint
#     report_response = requests.get(report_url, headers=headers)

#     my_reports = []
#     if Response(report_response).status_code == 200:
#         my_reports = report_response.json()

#     # appending report data to product dictionary
#     for report in my_reports:
#         for equipment in all_equipments:
#             if report["reported_equipment"] == equipment["id"]:
#                 equipment["reported"] = True
#             else:
#                 equipment["reported"] = False

#     report_categories = ["False Information", "Fake Equipments", "Misinformation", "Something Else"]
    
#     context = {
#         "all_equipments": all_equipments,
#         "categories": report_categories
#     } 

#     return render(request, 'buyers/allEquipments.html', context)


# @login_required
# @buyers_only
# def edit_eqp_comment(request):
#     comment_put_response = eqp_comment_edit(request)
    
#     if Response(comment_put_response).status_code == 200:
#         print('Comment Updated Successfully')
#     return redirect('/buyers/viewEquipments')


# @login_required
# @buyers_only
# def delete_eqp_comment(request, id):
#     comment_del_response = eqp_comment_delete(request, id)
    
#     if Response(comment_del_response).status_code == 200:
#         print('Deleted Successfully')
#     return redirect('/buyers/viewEquipments')


# @login_required
# @buyers_only
# def report_equipment(request):
#     headers = {'Authorization': 'Token ' + request.session['token']}
#     if request.method == 'POST':
#         data = request.POST
#         reported_equipment = data['eqp_id']
#         report_category = data['category']
#         report_description = data['description']
#         reported_by = request.user.id

#         report_data = {
#             "reported_by": reported_by,
#             "reported_equipment": reported_equipment,
#             "report_category": report_category,
#             "report_description": report_description
#         }

#         report_endpoint = '/api/equipment/reports'
#         report_url = base_url + report_endpoint
#         report_response = requests.post(report_url, data=report_data, headers=headers)
#         if Response(report_response).status_code == 200:
#             print("Equipment Reported Successfully")
#         return redirect('/buyers/viewEquipments')
