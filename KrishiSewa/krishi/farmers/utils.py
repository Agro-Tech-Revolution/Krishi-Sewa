import requests
import pickle
from rest_framework.response import Response
from api.views import *
from django.core.files.storage import default_storage
from PIL import Image


# base_url = "http://127.0.0.1:8000"

def comment_add(request, prod_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    data = request.POST
    product = prod_id
    comment = data['comment']
    comment_by = request.user.id

    request.data = {
        'comment_by': comment_by,
        'product': product,
        'comment': comment
    }

    comment_post_obj = ProductCommentView()
    comment_post_response = comment_post_obj.post(request)

    return comment_post_response
    

def comment_edit(request, comment_id):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        product = data["product"]
        comment = data['comment']
        comment_by = request.user.id

        request.data = {
            'comment_by': comment_by,
            'product': product,
            'comment': comment
        }

        comment_put_obj = CommentDetails()
        comment_put_response = comment_put_obj.put(request, comment_id)
        
        return comment_put_response


def comment_delete(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    comment_del_obj = CommentDetails()
    comment_del_response = comment_del_obj.delete(request, id)

    return comment_del_response


def comment_add_eqp(request, eqp_id):
    data = request.POST
    comment = data['comment']
    equipment = eqp_id
    comment_by = request.user.id

    request.data = {
        "comment_by": comment_by,
        "equipment": equipment,
        "comment": comment
    }

    comment_post_obj = EquipmentCommentView()
    comment_post_response = comment_post_obj.post(request)
    return comment_post_response


def update_profile_data(request, user_id, current_profile_pic):
    contact = None
    data = request.POST
    username = request.user.username
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    user = user_id
    bio = data["bio"]

    address = data["address"]
    
    if data["contact"] != '':
        try:
            contact_data = int(data["contact"])
            contact = contact_data
        except:
            return Response({"Bad Request": "Contact number should be numbers"})

    try:
        profile_pic = request.FILES["profile_pic"]
    except:
        profile_pic = None

    image_path = current_profile_pic
    if not profile_pic == None:
        try:
            Image.open(profile_pic)
            image_path = default_storage.save('static/profile_pic/' + str(profile_pic), profile_pic)
        except:
            return Response({"Bad Request": "Invalid image"})
    
    request.data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "user": user,
        "bio": bio,
        "contact": contact,
        "address": address,
        "profile_pic": image_path,
    }
    # print(data_to_update)
    update_profile_obj = UpdateProfileView()
    user_put_response = update_profile_obj.put(request, user_id)

    return user_put_response


def purchase_eqp_request(request, eqp_id):
    equipment_detail_obj = EquipmentsToDisplayDetails()
    equipment_detail_response = equipment_detail_obj.get(request, eqp_id).data
    price_per_item = equipment_detail_response["price_to_buy_per_item"]

    data = request.POST
    equipment = eqp_id
    sold_to = request.user.id
    quantity = data["quantity"]
    delivered_address = data['address']
    total_price = int(price_per_item) * int(quantity)
    remarks = data['remarks']

    request.data = {
        "equipment": equipment,
        "sold_to": sold_to,
        "quantity": quantity,
        "delivered_address": delivered_address,
        "total_price": total_price,
        "remarks": remarks,
    }
    
    buy_equipment_obj = BuyEquipmentView()
    buy_equipment_response = buy_equipment_obj.post(request)

    return buy_equipment_response


def rent_eqp_request(request, eqp_id):
    equipment_detail_obj = EquipmentsToDisplayDetails()
    equipment_detail_response = equipment_detail_obj.get(request, eqp_id).data
    price_per_hour = equipment_detail_response["price_per_hour"]

    data = request.POST
    equipment = eqp_id
    rented_to = request.user.id
    rented_quantity = data["quantity"]

    day = data["day"]
    hours = data["hours"]
    delivered_address = data['address']
    rented_duration = (int(day) * 24) + int(hours)
    total_price = rented_duration * int(rented_quantity) * int(price_per_hour)

    remarks = data['remarks']

    request.data = {
        "equipment": equipment,
        "rented_to": rented_to,
        "rented_quantity": rented_quantity,
        "delivered_address": delivered_address,
        "rented_duration": rented_duration,
        "total_price": total_price,
        "remarks": remarks,
    }
    
    rent_equipment_obj = RentEquipmentView()
    rent_equipment_response = rent_equipment_obj.post(request)
    return rent_equipment_response


def buy_eqp_req(request, action):
    eqp_request_obj = BoughtEquipmentsBuyer()
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
    return eqp_request, seen, approved


def rent_eqp_req(request, action):
    eqp_request_obj = RentedEquipmentsBuyer()
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
    return eqp_request, seen, approved


def eqp_approved(request, action):
    equipment_request_response = ""
    table = ""

    if action.upper() == "BOUGHT":
        eqp_request_obj = BoughtEquipmentsBuyer()
        equipment_request_response = eqp_request_obj.get(request, request.user.id).data
        table = "buy"
    elif action.upper() == "RENTED":
        eqp_request_obj = RentedEquipmentsBuyer()
        equipment_request_response = eqp_request_obj.get(request, request.user.id).data
        table = "rent"

    all_data = equipment_request_response
    eqp_request = [eqp_req for eqp_req in all_data if eqp_req["approved"]]
    return eqp_request, table


def edit_eqp_buy(request, req_id):
    eqp_req_obj = BuyEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)

    data = request.POST
    quantity = data["quantity"]
    delivered_address = data["address"]
    remarks = data["remarks"]
    total_price = float(quantity) * eqp_req_response.data["equipment"]["price_to_buy_per_item"]
    request.data = {
        "quantity": quantity,
        "delivered_address": delivered_address,
        "remarks": remarks,
        "total_price": total_price,
    }
    
    eqp_req_put_response = eqp_req_obj.put(request, req_id)
    return eqp_req_put_response

def edit_eqp_rent(request, req_id):
    eqp_req_obj = RentEquipmentDetails()
    eqp_req_response = eqp_req_obj.get(request, req_id)

    data = request.POST
    rented_quantity = data["quantity"]
    delivered_address = data["address"]
    remarks = data["remarks"]
    day = data["day"]
    hours = data["hours"]
    if day == "":
        day = 0
    if hours == "":
        hours = 0
    rented_duration = float(day) * 24 + float(hours)
    total_price = float(rented_quantity) * eqp_req_response.data["equipment"]["price_per_hour"] * rented_duration
    request.data = {
        "rented_quantity": rented_quantity,
        "rented_duration": rented_duration,
        "delivered_address": delivered_address,
        "remarks": remarks,
        "total_price": total_price,
    }
    
    eqp_req_put_response = eqp_req_obj.put(request, req_id)
    return eqp_req_put_response



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

    for i in crops.keys():
        if i == prediction:
            return crops[i]