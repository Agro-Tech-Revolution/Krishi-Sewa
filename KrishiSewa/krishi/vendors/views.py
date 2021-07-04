from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
from rest_framework.response import Response
from .utils import *

# Create your views here.
base_url = 'http://127.0.0.1:8000'


@login_required
@vendors_only
def index(request):
    return render(request, 'vendors/vendors.html')


@login_required
@vendors_only
def equipments(request):
    
    if request.method == 'POST':
        data = request.POST
        name = data['name']
        modal = data['modal']
        category = data['category']
        available_for_rent = data['rent']
        price_to_rent = data['rent_price']
        available_to_buy = data['buy']
        price_to_buy = data['buy_price']
        details = data['details']
        # eqp_img = request.FILES["image"]
        added_by = request.user.id

        equipment_data = {
            "name": name,
            "modal": modal,
            "category": category,
            "available_for_rent": available_for_rent == 'True',
            "price_to_rent": float(price_to_rent),
            "available_to_buy": available_to_buy == 'True',
            "price_to_buy": price_to_buy,
            "details": details,
            # "eqp_img": eqp_img,
            "added_by": added_by
        }
        
        equipment_post_endpoint = '/api/equipment/'
        equipment_post_url = base_url + equipment_post_endpoint
        headers = {'Authorization': 'Token ' + request.session['token']}

        equipment_post_response = requests.post(equipment_post_url, data=equipment_data, headers=headers)
        if Response(equipment_post_response).status_code == 200:
            print('Equipment added successfully' )
    
    categories = ['Tractor', 'Harvester', 'ATV or UTV', 'Plows' , 'Harrows',
                  'Fertilizer Spreaders', 'Seeders', 'Balers', 'Other']
    context = {
        'categories': categories
    }
    return render(request, 'vendors/addEquipments.html', context)


@login_required
@vendors_only
def my_equipments(request):
    headers = {'Authorization': 'Token ' + request.session['token']}

    if request.method=='POST':
        comment_post_response = eqp_comment_add(request)
        if Response(comment_post_response).status_code == 200:
            print('Comment Added Successfully')
            return redirect('/vendors/myEquipments')

    # calling equipment api to get all the equipments added by me
    equipment_get_endpoint = '/api/equipment/mine/' + str(request.user.id)
    equipment_get_url = base_url + equipment_get_endpoint
    equipment_get_response = requests.get(equipment_get_url, headers=headers)

    equipments_by_me = []
    if Response(equipment_get_response).status_code == 200:
        equipments_by_me = equipment_get_response.json()
        
    # calling comment api to get all the comments of equipments added by logged in user
    comment_endpoint = '/api/equipment/comments/user/' + str(request.user.id)
    comment_url = base_url + comment_endpoint
    comment_response = requests.get(comment_url, headers=headers)

    comments_on_my_equipments = []
    if Response(comment_response).status_code == 200:
        comments_on_my_equipments = comment_response.json()

    # modifiying comments keys and values so that the name of the person who commmented can be seen
    for comment in comments_on_my_equipments:
        user_endpoint = '/api/users/id/'+str(comment['comment_by'])
        user_url = base_url + user_endpoint
        user_response = requests.get(user_url, headers=headers)
        if Response(user_response).status_code == 200:
            comment['comment_by'] = user_response.json()

    # appending comments of a equipment to equipments dictionary
    for equipment in equipments_by_me:
        comments_for_a_equipment = []
        for comment in comments_on_my_equipments:
            if comment['equipment'] == equipment['id']:
                comments_for_a_equipment.append(comment)
        equipment['comments'] = comments_for_a_equipment
        
    context = {
        "my_equipments": equipments_by_me,
    }    

    return render(request, 'vendors/myEquipments.html', context)


@login_required
@vendors_only
def edit_equipment(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    if request.method == 'POST':
        data = request.POST
        name = data['name']
        modal = data['modal']
        category = data['category']
        available_for_rent = data['rent']
        price_to_rent = data['rent_price']
        available_to_buy = data['buy']
        price_to_buy = data['buy_price']
        details = data['details']
        # eqp_img = request.FILES["image"]
        added_by = request.user.id

        equipment_put_data = {
            "name": name,
            "modal": modal,
            "category": category,
            "available_for_rent": available_for_rent == 'True',
            "price_to_rent": float(price_to_rent),
            "available_to_buy": available_to_buy == 'True',
            "price_to_buy": price_to_buy,
            "details": details,
            # "eqp_img": eqp_img,
            "added_by": added_by
        }

        equipment_put_endpoint = '/api/equipment/'+str(id)
        equipment_put_url = base_url + equipment_put_endpoint

        equipment_put_response = requests.put(equipment_put_url, data=equipment_put_data, headers=headers)
        if Response(equipment_put_response).status_code == 200:

            print('Equipment updated successfully')
            return redirect('/vendors/myEquipments')


    equipment_get_endpoint = '/api/equipment/' + str(id)
    equipment_get_url = base_url + equipment_get_endpoint
    equipment_get_response = requests.get(equipment_get_url, headers=headers)
    if Response(equipment_get_response).status_code == 200:
        equipment_get_data = equipment_get_response.json()

    categories = ['Tractor', 'Harvester', 'ATV or UTV', 'Plows' , 'Harrows',
                  'Fertilizer Spreaders', 'Seeders', 'Balers', 'Other']
    context = {
        'equipment': equipment_get_data,
        'categories': categories
    }
    return render(request, 'vendors/editEquipments.html', context)


@login_required
@vendors_only
def delete_equipment(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    equipment_endpoint = '/api/equipment/' + str(id)
    equipment_url = base_url + equipment_endpoint
    equipment_response = requests.delete(equipment_url, headers=headers)
    if Response(equipment_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/vendors/myEquipments')


@login_required
@vendors_only
def edit_comment(request):
    comment_put_response = eqp_comment_edit(request)
    
    if Response(comment_put_response).status_code == 200:
        print('Comment Updated Successfully')
    return redirect('/vendors/myEquipments')


@login_required
@vendors_only
def delete_comment(request, id):
    comment_del_response = eqp_comment_delete(request, id)
    
    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/vendors/myEquipments')