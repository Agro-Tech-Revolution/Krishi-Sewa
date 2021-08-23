from django.db.models import base
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
from rest_framework.response import Response
from farmers.utils import *
from .utils import *
from django.core.files.storage import  default_storage
from PIL import Image
from api.views import *
from admins.api.views import *

# Create your views here.


@login_required
@vendors_only
def index(request):
    return render(request, 'vendors/vendors.html')


@login_required
@vendors_only
def equipments(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        price_to_buy_per_item = None
        price_per_hour = None
        duration = None

        data = request.POST
        equipment = data['equipment']
        modal = data['modal']
        available_for_rent = data['rent_availability']
        available_to_buy = data['buy_availability']
        details = data['details']
        
        added_by = request.user.id

        if available_for_rent.upper() == 'YES':
            price_per_hour = data['price_per_hour']
            duration = data['available_duration']

        if available_to_buy.upper() == 'YES':
            price_to_buy_per_item = data['price_to_buy']
        
        if price_per_hour == None and price_to_buy_per_item == None:
            print("Both rent and buy price cannot be empty")
            return redirect('/vendors/addEquipments')

        try:
            eqp_img = request.FILES["eqp_image"]
        except:
            eqp_img = None

        image_path = ''
        if not eqp_img == None:
            try:
                Image.open(eqp_img)
                image_path = default_storage.save('static/eqp_images/' + str(eqp_img), eqp_img)
            except:
                print("Not Valid Image")
                return redirect('/vendors/addEquipments')
        
        

        request.data = {
            "equipment": equipment,
            "modal": modal,
            "available_for_rent": available_for_rent == 'Yes',
            "price_per_hour": price_per_hour,
            "duration": duration,
            "available_to_buy": available_to_buy == 'Yes',
            "price_to_buy_per_item": price_to_buy_per_item,
            "details": details,
            "eqp_img": image_path,
            "added_by": added_by
        }
        equipment_post_obj = EquipmentsToDisplayView()
        equipment_post_response = equipment_post_obj.post(request)

        if equipment_post_response.data.get('id') != None:
            print('Equipment addedd successfully')
            return redirect('/vendors/addEquipments')
        else:
            error = equipment_post_response.data
            print(error)
        return redirect('/vendors/addEquipments')

    equipment_names_obj = EquipmentAPIView()
    equipment_names_response = equipment_names_obj.get(request)

    categories = ['Tractor', 'Harvester', 'ATV or UTV', 'Plows' , 'Harrows',
                  'Fertilizer Spreaders', 'Seeders', 'Balers', 'Other']
    context = {
        'categories': categories,
        'equipment_names': equipment_names_response.data
    }
    return render(request, 'vendors/addEquipments.html', context)


@login_required
@vendors_only
def my_equipments(request):

    categories = ['Tractor', 'Harvester', 'ATV or UTV', 'Plows' , 'Harrows',
                  'Fertilizer Spreaders', 'Seeders', 'Balers', 'Other']

    eqp_obj = MyEquipments()
    eqp_get_response = eqp_obj.get(request, request.user.id)
    context = {
        "categories": categories,
        "eqp_data": eqp_get_response.data
    }

    return render(request, 'vendors/myEquipments.html', context)


@login_required
@vendors_only
def equipment_details(request, eqp_id):
    if request.method == 'POST':
        comment_post_response = comment_add_eqp(request, eqp_id)

        if comment_post_response.data.get('id') != None:
            print('Comment submitted successfully')
            return redirect('/vendors/myEquipments/' + str(eqp_id))
        else:
            error = comment_post_response.data
            print(error)
            return redirect('/vendors/myEquipments/' + str(eqp_id))

    eqp_detail_obj = EquipmentsToDisplayDetails()
    eqp_detail_response = eqp_detail_obj.get(request, eqp_id)

    eqp_data = eqp_detail_response.data
    if eqp_data.get('id') != None:
        user_id = eqp_data.get('added_by').get('id')
        if user_id != request.user.id:
            eqp_data = ''
    
    context = {
        'eqp_data': eqp_data
    }


    return render(request, 'vendors/equipmentDetails.html', context)


@login_required
@vendors_only
def edit_equipment(request, eqp_id):

    eqp_detail_obj = EquipmentsToDisplayDetails()
    eqp_detail_response = eqp_detail_obj.get(request, eqp_id)

    eqp_data = eqp_detail_response.data
    if eqp_data.get('id') != None:
        user_id = eqp_data.get('added_by').get('id')
        if user_id != request.user.id:
            eqp_data = ''

    if request.method == 'POST':
        price_to_buy_per_item = None
        price_per_hour = None
        duration = None

        data = request.POST
        equipment = data['equipment']
        modal = data['modal']
        available_for_rent = data['rent_availability']
        available_to_buy = data['buy_availability']
        details = data['details']
        
        added_by = request.user.id

        if available_for_rent.upper() == 'YES':
            price_per_hour = data['price_per_hour']
            duration = data['available_duration']

        if available_to_buy.upper() == 'YES':
            price_to_buy_per_item = data['price_to_buy']
        
        if price_per_hour == None and price_to_buy_per_item == None:
            print("Both rent and buy price cannot be empty")
            return redirect('/vendors/editEquipment/' + str(eqp_id))

        try:
            eqp_img = request.FILES["eqp_image"]
        except:
            eqp_img = None

        image_path = ''
        if not eqp_img == None:
            try:
                Image.open(eqp_img)
                image_path = default_storage.save('static/eqp_images/' + str(eqp_img), eqp_img)
            except:
                print("Not Valid Image")
                return redirect('/vendors/editEquipment/' + str(eqp_id))
        else:
            image_path = eqp_data.get('eqp_img')

        request.data = {
            "equipment": equipment,
            "modal": modal,
            "available_for_rent": available_for_rent == 'Yes',
            "price_per_hour": price_per_hour,
            "duration": duration,
            "available_to_buy": available_to_buy == 'Yes',
            "price_to_buy_per_item": price_to_buy_per_item,
            "details": details,
            "eqp_img": image_path,
            "added_by": added_by
        }

        equipment_put_response = eqp_detail_obj.put(request, eqp_id)

        if equipment_put_response.data.get('id') != None:
            print('Equipment updated successfully')
            return redirect('/vendors/myEquipments')
        else:
            error = equipment_put_response.data
            print(error)
        return redirect('/vendors/editEquipment/' + str(eqp_id))

    equipment_names_obj = EquipmentAPIView()
    equipment_names_response = equipment_names_obj.get(request)

    categories = ['Tractor', 'Harvester', 'ATV or UTV', 'Plows' , 'Harrows',
                  'Fertilizer Spreaders', 'Seeders', 'Balers', 'Other']
    context = {
        'eqp_data': eqp_data,
        'categories': categories,
        'equipment_names': equipment_names_response.data
    }
    return render(request, 'vendors/editEquipments.html', context)


@login_required
@vendors_only
def delete_equipment(request, eqp_id):
    eqp_detail_obj = EquipmentsToDisplayDetails()
    eqp_get_response = eqp_detail_obj.get(request, eqp_id).data
    
    if eqp_get_response.get('added_by').get('id') == request.user.id:
        eqp_del_response = eqp_detail_obj.delete(request, eqp_id)    
        if Response(eqp_del_response).status_code == 200:
            print('Deleted Successfully')
    else:
        print("Not your equipment")
    
    return redirect('/vendors/myEquipments')


@login_required
@vendors_only
def edit_comment(request):
    pass
    # comment_put_response = eqp_comment_edit(request)
    
    # if Response(comment_put_response).status_code == 200:
    #     print('Comment Updated Successfully')
    # return redirect('/vendors/myEquipments')


@login_required
@vendors_only
def delete_comment(request, id):
    pass
    # comment_del_response = eqp_comment_delete(request, id)
    
    # if Response(comment_del_response).status_code == 200:
    #     print('Deleted Successfully')
    # return redirect('/vendors/myEquipments')


@login_required
@vendors_only
def profile(request, user_id):
    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id)
    context = {
        'user_data': user_detail_response.data
    }
    return render(request, 'vendors/profile.html', context)



@login_required
@vendors_only
def edit_profile(request, user_id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    user_detail_obj = GetUserDetails()
    user_detail_response = user_detail_obj.get(request, user_id).data

    current_profile_pic = user_detail_response["profile_pic"]

    if request.method == 'POST':
        user_put_response = update_profile_data(request, user_id, current_profile_pic)
        if user_put_response.data.get('username') != None:
            print('Profile updated successfully')
            return redirect('/vendors/profile/' + str(user_id))
        else:
            error = user_put_response.data
            print(error)
        return redirect('/vendors/profile/' + str(user_id) + '/edit')

    context = {
        'user_data': user_detail_response
    }
    return render(request, 'vendors/editProfile.html', context)


@login_required
@vendors_only
def equipment_requests(request, action=None):
    pass


@login_required
@vendors_only
def approve_eqp_buy_request(request, eqp_req_id):
    request.data = {
        "approved": True
    }
    eqp_req_obj = ChangeEqpBuyRequestStatus()
    eqp_req_response = eqp_req_obj.put(request, eqp_req_id)
    if eqp_req_response.data.get("success") != None:
        print(eqp_req_response.data)
    else:
        print(eqp_req_response.data)
    return redirect('/vendors/eqpBuyRequests')


@login_required
@vendors_only
def disapprove_eqp_buy_request(request, eqp_req_id):
    request.data = {
        "approved": False
    }
    eqp_req_obj = ChangeEqpBuyRequestStatus()
    eqp_req_response = eqp_req_obj.put(request, eqp_req_id)
    if eqp_req_response.data.get("success") != None:
        print(eqp_req_response.data)
    else:
        print(eqp_req_response.data)
    return redirect('/vendors/eqpBuyRequests')



@login_required
@vendors_only
def equipment_bought_requests(request, action=None):
    eqp_request_obj = SoldEquipmentSeller()
    equipment_request_response = eqp_request_obj.get(request, request.user.id)
    all_data = equipment_request_response.data
    
    eqp_request = []
    seen = ""
    approved = ""
    if action == None:
        eqp_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and not eqp_req["seen"]]
        seen = False
        approved = False
    elif action == 'approved':
        eqp_request = [eqp_req for eqp_req in all_data if eqp_req["approved"]]
        seen = True
        approved = True
    elif action == 'disapproved':
        eqp_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and eqp_req["seen"]]
        seen = True
        approved = False

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'vendors/eqpBuyRequests.html', context)


@login_required
@vendors_only
def equipment_rented_requests(request, action=None):
    eqp_request_obj = RentedEquipmentSeller()
    equipment_request_response = eqp_request_obj.get(request, request.user.id)
    all_data = equipment_request_response.data
    
    eqp_request = []
    seen = ""
    approved = ""
    if action == None:
        eqp_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and not eqp_req["seen"]]
        seen = False
        approved = False
    elif action == 'approved':
        eqp_request = [eqp_req for eqp_req in all_data if eqp_req["approved"]]
        seen = True
        approved = True
    elif action == 'disapproved':
        eqp_request = [eqp_req for eqp_req in all_data if not eqp_req["approved"] and eqp_req["seen"]]
        seen = True
        approved = False

    context = {
        "eqp_request": eqp_request,
        "seen": seen,
        "approved": approved
    }

    return render(request, 'vendors/eqpRentRequests.html', context)


@login_required
@vendors_only
def approve_eqp_rent_request(request, eqp_req_id):
    request.data = {
        "approved": True
    }
    eqp_req_obj = ChangeEqpRentRequestStatus()
    eqp_req_response = eqp_req_obj.put(request, eqp_req_id)
    if eqp_req_response.data.get("success") != None:
        print(eqp_req_response.data)
    else:
        print(eqp_req_response.data)
    return redirect('/vendors/eqpRentRequests')


@login_required
@vendors_only
def disapprove_eqp_rent_request(request, eqp_req_id):
    request.data = {
        "approved": False
    }
    eqp_req_obj = ChangeEqpRentRequestStatus()
    eqp_req_response = eqp_req_obj.put(request, eqp_req_id)
    if eqp_req_response.data.get("success") != None:
        print(eqp_req_response.data)
    else:
        print(eqp_req_response.data)
    return redirect('/vendors/eqpRentRequests')


@login_required
@vendors_only
def my_sales(request, action=None):
    
    buy_req_obj = SoldEquipmentSeller()
    rent_req_obj = RentedEquipmentSeller()
    

    buy_req_response = buy_req_obj.get(request, request.user.id)
    rent_req_response = rent_req_obj.get(request,request.user.id)

    buy_data = buy_req_response.data
    rent_data = rent_req_response.data

    buy_req = [eqp_req for eqp_req in buy_data if eqp_req["approved"]]
    rent_req = [eqp_req for eqp_req in rent_data if eqp_req["approved"]]

    if action == None:
        pass
    elif action == 'buy':
        rent_req = []
    elif action == 'rent':
        buy_req = []
    else:
        buy_req = []
        rent_req = []

    context = {
        "my_sales": buy_req + rent_req
    }
    return render(request, 'vendors/Mysales.html', context)