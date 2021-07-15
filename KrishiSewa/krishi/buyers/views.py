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


@login_required
@buyers_only
def view_products(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method=='POST':
        comment_post_response = comment_add(request)
        if Response(comment_post_response).status_code == 200:
            print('Comment Added Successfully')
            return redirect('/buyers/viewProducts')
    
    product_endpoint = '/api/products/' 
    product_url = base_url + product_endpoint
    product_response = requests.get(product_url, headers=headers)

    all_products = []
    if Response(product_response).status_code == 200:
        all_products = product_response.json()

    # calling comment api to get all the comments 
    comment_endpoint = '/api/products/comments'
    comment_url = base_url + comment_endpoint
    comment_response = requests.get(comment_url, headers=headers)

    all_comments = []
    if Response(comment_response).status_code == 200:
        all_comments = comment_response.json()

    # modifiying comments keys and values so that the name of the person who commmented can be seen
    for comment in all_comments:
        user_endpoint = '/api/users/id/'+str(comment['comment_by'])
        user_url = base_url + user_endpoint
        user_response = requests.get(user_url, headers=headers)
        if Response(user_response).status_code == 200:
            comment['comment_by'] = user_response.json()
    
    # appending comments of a product to products dictionary
    for products in all_products:
        comments_for_a_product = []
        for comment in all_comments:
            if comment['product'] == products['id']:
                comments_for_a_product.append(comment)
        products['comments'] = comments_for_a_product

    # calling report api to find all the products that the logged in user has reported
    report_endpoint = '/api/products/reports/users/' + str(request.user.id)
    report_url = base_url + report_endpoint
    report_response = requests.get(report_url, headers=headers)

    my_reports = []
    if Response(report_response).status_code == 200:
        my_reports = report_response.json()

    # appending report data to product dictionary
    for report in my_reports:
        for product in all_products:
            if report["reported_product"] == product["id"]:
                product["reported"] = True
            else:
                product["reported"] = False

    report_categories = ["False Information", "Fake Products", "Misinformation", "Something Else"]
    
    context = {
        "all_products": all_products,
        "categories": report_categories
    } 

    return render(request, 'buyers/allProducts.html', context)


@login_required
@buyers_only
def edit_comment(request):
    comment_put_response = comment_edit(request)
    
    if Response(comment_put_response).status_code == 200:
        print('Comment Updated Successfully')
    return redirect('/buyers/viewProducts')


@login_required
@buyers_only
def delete_comment(request, id):
    comment_del_response = comment_delete(request, id)
    
    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/buyers/viewProducts')


@login_required
@buyers_only
def report_product(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        reported_product = data['prod_id']
        report_category = data['category']
        report_description = data['description']
        reported_by = request.user.id

        report_data = {
            "reported_by": reported_by,
            "reported_product": reported_product,
            "report_category": report_category,
            "report_description": report_description
        }

        report_endpoint = '/api/products/reports'
        report_url = base_url + report_endpoint
        report_response = requests.post(report_url, data=report_data, headers=headers)
        if Response(report_response).status_code == 200:
            print("Product Reported Successfully")
        return redirect('/buyers/viewProducts')


# equipments start
@login_required
@buyers_only
def view_equipments(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method=='POST':
        comment_post_response = eqp_comment_add(request)
        if Response(comment_post_response).status_code == 200:
            print('Comment Added Successfully')
            return redirect('/buyers/viewEquipments')
    
    equipment_get_endpoint = '/api/equipment/' 
    equipmet_get_url = base_url + equipment_get_endpoint
    equipment_get_response = requests.get(equipmet_get_url, headers=headers)

    all_equipments = []
    if Response(equipment_get_response).status_code == 200:
        all_equipments = equipment_get_response.json()

    # calling comment api to get all the comments 
    comment_endpoint = '/api/equipment/comments'
    comment_url = base_url + comment_endpoint
    comment_response = requests.get(comment_url, headers=headers)

    all_comments = []
    if Response(comment_response).status_code == 200:
        all_comments = comment_response.json()

    # modifiying comments keys and values so that the name of the person who commmented can be seen
    for comment in all_comments:
        user_endpoint = '/api/users/id/'+str(comment['comment_by'])
        user_url = base_url + user_endpoint
        user_response = requests.get(user_url, headers=headers)
        if Response(user_response).status_code == 200:
            comment['comment_by'] = user_response.json()
    
    # appending comments of a equipment to equipments dictionary
    for equipment in all_equipments:
        comments_for_a_equipment = []
        for comment in all_comments:
            if comment['equipment'] == equipment['id']:
                comments_for_a_equipment.append(comment)
        equipment['comments'] = comments_for_a_equipment

    # calling report api to find all the equipments that the logged in user has reported
    report_endpoint = '/api/equipment/reports/users/' + str(request.user.id)
    report_url = base_url + report_endpoint
    report_response = requests.get(report_url, headers=headers)

    my_reports = []
    if Response(report_response).status_code == 200:
        my_reports = report_response.json()

    # appending report data to product dictionary
    for report in my_reports:
        for equipment in all_equipments:
            if report["reported_equipment"] == equipment["id"]:
                equipment["reported"] = True
            else:
                equipment["reported"] = False

    report_categories = ["False Information", "Fake Equipments", "Misinformation", "Something Else"]
    
    context = {
        "all_equipments": all_equipments,
        "categories": report_categories
    } 

    return render(request, 'buyers/allEquipments.html', context)


@login_required
@buyers_only
def edit_eqp_comment(request):
    comment_put_response = eqp_comment_edit(request)
    
    if Response(comment_put_response).status_code == 200:
        print('Comment Updated Successfully')
    return redirect('/buyers/viewEquipments')


@login_required
@buyers_only
def delete_eqp_comment(request, id):
    comment_del_response = eqp_comment_delete(request, id)
    
    if Response(comment_del_response).status_code == 200:
        print('Deleted Successfully')
    return redirect('/buyers/viewEquipments')


@login_required
@buyers_only
def report_equipment(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        reported_equipment = data['eqp_id']
        report_category = data['category']
        report_description = data['description']
        reported_by = request.user.id

        report_data = {
            "reported_by": reported_by,
            "reported_equipment": reported_equipment,
            "report_category": report_category,
            "report_description": report_description
        }

        report_endpoint = '/api/equipment/reports'
        report_url = base_url + report_endpoint
        report_response = requests.post(report_url, data=report_data, headers=headers)
        if Response(report_response).status_code == 200:
            print("Equipment Reported Successfully")
        return redirect('/buyers/viewEquipments')
