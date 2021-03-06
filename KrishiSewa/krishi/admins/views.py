from django.shortcuts import render
from accounts.auth import *
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.core.files.storage import  default_storage
from PIL import Image
from admins.api.views import *
from farmers.utils import update_profile_data
from django.contrib import messages

# Create your views here.

@login_required
@admin_only
def index(request):
    return render(request, 'admins/admins.html')


@login_required
@admin_only
def dashboard(request):
    db_obj = DashboardView()
    db_response = db_obj.get(request)
    context = {
        'db_data': db_response.data
    }
    return render(request, 'admins/DB.html', context)


@login_required
@admin_only
def test(request):
    return render(request, 'admins/dashboard.html')


@login_required
@admin_only
def add_products(request):
    prod_obj = ProductsAPIView()
    if request.method == 'POST':
        data = request.POST
        prod_name = data['name']
        prod_category = data['category']
        
        try:
            prod_img = request.FILES["image"]
        except:
            prod_img = None
        
        image_path = ''
        if not prod_img == None:
            try:
                Image.open(prod_img)
                image_path = default_storage.save('static/product_images/' + str(prod_img), prod_img)
            except:
                messages.error(request, "Not valid image")
                return redirect('/admins/addProducts/')

        request.data = {
            "prod_name": prod_name,
            "prod_category": prod_category,
            "prod_img": image_path,
        }
        
        
        product_response = prod_obj.post(request)
        # print(product_response.json().get('id'))
        if product_response.data.get('id') != None:
            messages.success(request, "Product added successfully")
        else:
            error = product_response.data
            messages.error(request, error)
    
    all_products = prod_obj.get(request)

    categories = ["Cereals", "Pulses", "Vegetables", "Fruits", "Nuts", "Oilseeds",
                  "Sugars and Starches", "Fibres", "Beverages", "Narcotics", "Spices", 
                  "Condiments", "Others"]
    context = {
        "categories": categories,
        "all_products": all_products.data
    }
    
    return render(request, 'admins/addProducts.html', context)


@login_required
@admin_only
def edit_product_details(request, prod_id):
    prod_obj = ProductDetails()
    prod_data = prod_obj.get(request, prod_id).data

    if request.method == 'POST':
        data = request.POST
        prod_name = data["name"]
        prod_category = data["category"]

        try:
            prod_img = request.FILES["image"]
        except:
            prod_img = None
        
        image_path = prod_data["prod_img"]
        if not prod_img == None:
            try:
                Image.open(prod_img)
                image_path = default_storage.save('static/product_images/' + str(prod_img), prod_img)
            except:
                messages.error(request, "Not valid image")
                return redirect('/admins/addProducts/')

        request.data = {
            "prod_name": prod_name,
            "prod_category": prod_category,
            "prod_img": image_path,
        }
        
        product_response = prod_obj.put(request, prod_id)
        if product_response.data.get('id') != None:
            messages.success(request, "Updated successfully")
            return redirect('/admins/addProducts/')
        else:
            error = product_response.data
            messages.error(request, error)
            return redirect('/admins/editProducts/' + str(prod_id))

    categories = ["Cereals", "Pulses", "Vegetables", "Fruits", "Nuts", "Oilseeds",
                  "Sugars and Starches", "Fibres", "Beverages", "Narcotics", "Spices", 
                  "Condiments", "Others"]
    context = {
        "categories": categories,
        "product": prod_data
    }
    return render(request, 'admins/editProducts.html', context)


@login_required
@admin_only
def delete_product(request, prod_id):
    prod_obj = ProductDetails()
    prod_response = prod_obj.delete(request, prod_id)
    if Response(prod_response).status_code == 200:
        messages.success(request, "Deleted successfully")
    return redirect('/admins/addProducts/')


@login_required
@admin_only
def add_equipments(request):
    eqp_obj = EquipmentAPIView()
    if request.method == 'POST':
        data = request.POST
        name = data["name"]
        category = data["category"]

        request.data = {
            'name': name,
            'category': category
        }

        eqp_post_response = eqp_obj.post(request)
        if eqp_post_response.data.get('id') != None:
            messages.success(request, "Equipment added successfully")
        else:
            error = eqp_post_response.data
            messages.error(request, error)
        return redirect('/admins/addEquipments/')

    all_equipments = eqp_obj.get(request)

    categories = [ "Tractor", "Harvester", "ATV or UTV", "Plows", "Harrows",
                    "Fertilizer Spreaders", "Seeders", "Balers", "Other",]
    context = {
        "categories": categories,
        "all_equipments" : all_equipments.data,
    } 

    return render(request, 'admins/addEquipments.html', context)


@login_required
@admin_only
def edit_equipment_details(request, eqp_id):
    eqp_obj = EquipmentDetails()
    eqp_data = eqp_obj.get(request, eqp_id).data

    if request.method == 'POST':
        data = request.POST 
        name = data["name"]
        category = data["category"]

        request.data = {
            'name': name,
            'category': category
        }

        eqp_response = eqp_obj.put(request, eqp_id)
        if eqp_response.data.get('id') != None:
            messages.success(request, "Updated successfully")
            return redirect('/admins/addEquipments/')
        else:
            error = eqp_response.data
            messages.error(request, error)
            return redirect('/admins/editEquipments/' + str(eqp_id))

    categories = [ "Tractor", "Harvester", "ATV or UTV", "Plows", "Harrows",
                    "Fertilizer Spreaders", "Seeders", "Balers", "Other",]
    context = {
        "categories": categories,
        "equipment" : eqp_data,
    } 

    return render(request, 'admins/editEquipments.html', context)


@login_required
@admin_only
def delete_equipment(request, eqp_id):
    eqp_obj = EquipmentDetails()
    eqp_response = eqp_obj.delete(request, eqp_id)
    if Response(eqp_response).status_code == 200:
        messages.success(request, "Deleted successfully")
    return redirect('/admins/addEquipments/')


@login_required
@admin_only  
def users(request):
    user_obj = AvailableUsersView()
    all_users = user_obj.get(request).data 
    context = {
        'all_users': all_users
    }

    return render(request, 'admins/users.html', context)


@login_required
@admin_only
def disable_user_account(request, user_id):
    request.data = {
        'is_active': False
    }
    action_obj = ActionOnUserView()
    action_response = action_obj.put(request, user_id)
    if action_response.data.get('success') != None:
        messages.success(request, "Account disabled")
    else:
        messages.error(request, action_response.data)
    return redirect('/admins/users/')


@login_required
@admin_only
def activate_user_account(request, user_id):
    request.data = {
        'is_active': True
    }
    action_obj = ActionOnUserView()
    action_response = action_obj.put(request, user_id)
    if action_response.data.get('success') != None:
        messages.success(request, "Account activated")
    else:
        messages.error(request, action_response.data)
    return redirect('/admins/users/')


@login_required
@admin_only
def report_user(request):
    report_obj = ReportUserView()
    report_data = report_obj.get(request).data
    context = {
        "report_data": report_data
    }
    return render(request, 'admins/reportUsers.html', context)


@login_required
@admin_only
def report_equipment(request):
    report_obj = EqpReports()
    report_data = report_obj.get(request).data
    context = {
        "report_data": report_data
    }
    return render(request, 'admins/reportEquipment.html', context)


@login_required
@admin_only
def report_product(request):
    report_obj = ProdReports()
    report_data = report_obj.get(request).data
    context = {
        "report_data": report_data
    }
    return render(request, 'admins/reportProduct.html', context)


@login_required
@admin_only
def famers(request):
    db_obj = DashboardView()
    db_response = db_obj.get(request)
    context = {
        'db_data': db_response.data
    }
    return render(request, 'admins/farmers/farmers.html', context)


@login_required
@admin_only
def vendors(request):
    db_obj = DashboardView()
    db_response = db_obj.get(request)
    context = {
        'sales_data': db_response.data
    }

    return render(request, 'admins/vendors/vendors.html', context)


@login_required
@admin_only
def buyers(request):
    db_obj = DashboardView()
    db_response = db_obj.get(request)
    context = {
        'prod_data': db_response.data
    }
    return render(request, 'admins/buyers/buyers.html', context)


@login_required
@admin_only
def farmer_list(request):
    farmer_obj = FarmersListView()
    farmer_data = farmer_obj.get(request).data 
    context = {
        "all_farmers": farmer_data
    }

    return render(request, 'admins/farmers/farmer_list.html', context)


@login_required
@admin_only
def vendors_list(request):
    vendor_obj = VendorsListView()
    vendor_data = vendor_obj.get(request).data 
    context = {
        "all_vendors": vendor_data
    }
    return render(request, 'admins/vendors/vendor_list.html', context)


@login_required
@admin_only
def buyers_list(request):
    buyer_obj = BuyersListView()
    buyer_data = buyer_obj.get(request).data 
    context = {
        "all_buyers": buyer_data
    }
    return render(request, 'admins/buyers/buyers_list.html', context)


@login_required
@admin_only
def create_ticket(request, category, link_id, user_id):
    if request.method == 'POST':
        data = request.POST
        title = data["title"]
        description = data["description"]
        link = "/"
        if category == 'equipment':
            link = '/vendors/myEquipments/'+str(link_id)
        elif category == 'product':
            link = '/farmers/myproducts/'+str(link_id)
        elif category == 'user':
            user_type_obj = GetProfileType()
            user_type_data = user_type_obj.get(request, user_id).data
            user_type = user_type_data["user_type"]
            link = '/' + user_type.lower() + '/profile/'+str(user_id)
        
        request.data = {
            "title": title,
            "description": description,
            "link": link,
            "category": category.capitalize(),
            "ticket_to": user_id
        }

        ticket_obj = TicketView()
        ticket_response = ticket_obj.post(request)
        if ticket_response.data.get('id') != None:
            messages.success(request, "Ticket created successfully")
        else:
            messages.error(request, ticket_response.data)
    return redirect('/admins/report'+category.capitalize())


@login_required
@admin_only
def view_ticket(request):
    all_ticket_obj = TicketView()
    all_ticket_data = all_ticket_obj.get(request).data
    
    context = {
        "all_tickets": all_ticket_data
    }
    return render(request, 'admins/viewTicket.html', context)


@login_required
@admin_only
def update_ticket_status(request, ticket_id):
    request.data = {
        "status": "Resolved"
    }
    update_obj = UpdateTicketStatus()
    update_obj_response = update_obj.put(request, ticket_id)
    if update_obj_response.data.get('success') != None:
        messages.success(request, "Ticket resolved")
    else:
        messages.error(request, update_obj_response.data)
    return redirect('/admins/tickets')

@login_required
@admin_only
def profile(request, user_id):
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
    return render(request, 'admins/profile.html', context)


@login_required
@admin_only
def edit_profile(request, user_id):

    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id).data

    current_profile_pic = user_detail_response["profile_pic"]

    if request.method == 'POST':
        user_put_response = update_profile_data(request, user_id, current_profile_pic)
        if user_put_response.data.get('username') != None:
            messages.success(request, "Profile updated successfully")
            return redirect('/admins/profile/' + str(user_id))
        else:
            error = user_put_response.data
            messages.error(request, error)
        return redirect('/admins/profile/' + str(user_id) + '/edit')       

    context = {
        'user_data': user_detail_response
    }
    return render(request, 'admins/editProfile.html', context)


@login_required
@admin_only
def change_password(request):
    return render(request, 'admins/changePassword.html')

@login_required
@admin_only
def view_feedback(request):
    all_feedback_obj = FeedbackView()
    all_feedback_data = all_feedback_obj.get(request).data
    
    context = {
        "all_feedbacks": all_feedback_data
    }
    return render(request, 'admins/viewFeedback.html', context)

