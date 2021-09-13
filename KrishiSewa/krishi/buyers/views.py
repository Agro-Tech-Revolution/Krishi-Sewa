from django.shortcuts import render
from accounts.auth import *
from django.contrib.auth.decorators import login_required
from farmers.utils import *
from vendors.utils import *
from admins.api.views import *
from django.contrib import messages

# Create your views here.
@login_required
@buyers_only
def index(request):
    return render(request, 'buyers/buyers.html')

@login_required
@buyers_only
def report_form(request):
    return render(request, 'buyers/ReportForm.html')

@login_required
@buyers_only
def feedback(request):
    return render(request, 'buyers/user-feedback.html')


# products start
@login_required
@buyers_only
def all_products(request):
    prod_display_obj = ProductsForSaleView()
    all_product_response = prod_display_obj.get(request)
    prod_data = all_product_response.data

    if request.method == 'POST':
        prod_data = search_prod(request)

    prod_reported = []
    for prod in prod_data:
        for prod_reports in prod["product_reports"]:
            if prod_reports["reported_by"]["id"] == request.user.id:
                prod_reported.append(prod)

    for prod in prod_reported:
        prod_data.remove(prod)


    categories = ['Cereals', 'Pulses', 'Vegetables', 'Fruits', 'Nuts', 'Oilseeds',
                  'Sugars and Starches', 'Fibres', 'Beverages', 'Narcotics',
                  'Spices', 'Condiments', 'Others']

    context = {
        "all_products": prod_data,
        "user_type": 'buyers',
        "categories": categories
    }

    return render(request, 'buyers/allProducts.html', context)


@login_required
@buyers_only
def product_details(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        comment_post_response = comment_add(request, prod_id)

        if comment_post_response.data.get('id') != None:
            messages.success(request, "Comment submitted successfully")
            return redirect('/buyers/productdetails/' + str(prod_id))
        else:
            error = comment_post_response.data
            messages.error(request, error)
            return redirect('/buyers/productdetails/' + str(prod_id))

    product_detail_obj = ProductsForSaleDetails()
    product_detail_response = product_detail_obj.get(request, prod_id)
    
    report_category = ["False Information", "Fake Products", "Misinformation",  "Something Else"]
    if len(product_detail_response.data) > 0:
        prod_report_data = product_detail_response.data.get('product_reports') 
        reported = False
        for report in prod_report_data:
            if report["reported_by"]["id"] == request.user.id:
                reported = True
                break
    else:
        reported = True

    context = {
        "product_detail": product_detail_response.data,
        "report_category": report_category,
        "reported": reported
    }
    return render(request, 'buyers/productDetails.html', context)


@login_required
@buyers_only
def report_prod_view(request, prod_id):
    if request.method == 'POST':
        data = request.POST 
        report_category = data["report-category"]
        report_description = data["description"]
        reported_by = request.user.id
        reported_product = prod_id

        request.data = {
            "report_category": report_category,
            "report_description": report_description,
            "reported_by": reported_by,
            "reported_product": reported_product,
        }

        prod_report_obj = ProductReportView()
        prod_report_response = prod_report_obj.post(request)
        if prod_report_response.data.get('id') != 'None':
            messages.success(request, "Reported Successfully")
        else:
            messages.error(request, prod_report_response.data)
            return redirect('/buyers/productdetails/'+str(prod_id))

    return redirect('/buyers/allProducts/')


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
            messages.success(request, "Request submitted successfully")
            return redirect('/buyers/allProducts/')
        else:
            error = buy_product_response.data
            messages.error(request, error)
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
            messages.success(request, "Updated successfully")
        else:
            messages.error(request, prod_req_put_response.data)
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
                messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "Sorry cannot perform the request")
    return redirect('/buyers/prodBuyRequests')



# equipments start
@login_required
@buyers_only
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
            messages.success(request, "Comment submitted successfully")
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))
        else:
            error = comment_post_response.data
            messages.error(request, error)
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))

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
    return render(request, 'buyers/equipmentDetails.html', context)


@login_required
@buyers_only
def report_eqp_view(request, eqp_id):
    if request.method == 'POST':
        eqp_report_response = report_eqp(request, eqp_id)
        if eqp_report_response.data.get('id') != 'None':
            messages.success(request, "Reported successfully")
        else:
            messages.error(request, eqp_report_response.data)
            return redirect('/buyers/equipmentDetails/'+str(eqp_id))

    return redirect('/buyers/allEquipments/')


@login_required
@buyers_only
def purchase_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        buy_equipment_response = purchase_eqp_request(request, eqp_id)

        if buy_equipment_response.data.get('id') != None:
            messages.success(request, "Request submitted successfully")
            return redirect('/buyers/allEquipments/')
        else:
            error = buy_equipment_response.data
            messages.error(request, error)
            return redirect('/buyers/equipmentdetails/' + str(eqp_id))

    return redirect('/buyers/equipmentdetails/' + str(eqp_id))


@login_required
@buyers_only
def rent_request(request, eqp_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        rent_equipment_response = rent_eqp_request(request, eqp_id)
        
        if rent_equipment_response.data.get('id') != None:
            messages.success(request, "Rent submitted successfully")
            return redirect('/buyers/allEquipments/')
        else:
            error = rent_equipment_response.data
            messages.error(request, error)
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
            messages.success(request, "Updated successfully")
        else:
            messages.error(request, eqp_req_put_response.data)
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
                messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "Sorry cannot perform the request")
    return redirect('/buyers/eqpBuyRequests')


@login_required
@buyers_only
def edit_eqp_rent_requests(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)
    
    if request.method == 'POST':
        eqp_req_put_response = edit_eqp_rent(request, req_id)
        if eqp_req_put_response.data.get('id') != None:
            messages.success(request, "Updated successfully")
        else:
            messages.error(request, eqp_req_put_response.data)
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
                messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "Sorry cannot perform the request")
    return redirect('/buyers/eqpRentRequests')


@login_required
@buyers_only
def profile(request, user_id):
    # headers = {'Authorization': 'Token ' + request.session['token']}
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
    return render(request, 'buyers/profile.html', context)


@login_required
@buyers_only
def edit_profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id).data

    current_profile_pic = user_detail_response["profile_pic"]

    if request.method == 'POST':
        user_put_response = update_profile_data(request, user_id, current_profile_pic)
        if user_put_response.data.get('username') != None:
            messages.success(request, "Profile updated successfully")
            return redirect('/buyers/profile/' + str(user_id))
        else:
            error = user_put_response.data
            messages.error(request, error)
        return redirect('/buyers/profile/' + str(user_id) + '/edit')       

    context = {
        'user_data': user_detail_response
    }
    return render(request, 'buyers/editProfile.html', context)


@login_required
@buyers_only
def view_ticket(request):
    my_ticket_obj = MyTickets()
    my_ticket_data = my_ticket_obj.get(request, request.user.id).data
    
    context = {
        "all_tickets": my_ticket_data
    }
    return render(request, 'buyers/viewTicket.html', context)

@login_required
@buyers_only
def change_password(request):
    return render(request, 'buyers/changePassword.html')


