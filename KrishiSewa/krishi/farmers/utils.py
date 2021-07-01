import requests
from rest_framework.response import Response


base_url = "http://127.0.0.1:8000"

def comment_add(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    data = request.POST
    product = data['prod_id']
    comment = data['comment']
    comment_by = request.user.id

    comment_data = {
        'comment_by': comment_by,
        'product': product,
        'comment': comment
    }

    comment_post_endpoint = '/api/products/comments'
    comment_post_url = base_url + comment_post_endpoint
    comment_post_response = requests.post(comment_post_url, data=comment_data, headers=headers)
    return comment_post_response
    

def comment_edit(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    if request.method == 'POST':
        data = request.POST
        comment_id = data['comment_id']
        product = data['prod_id']
        comment = data['comment']
        comment_by = request.user.id

        comment_data = {
            'comment_by': comment_by,
            'product': product,
            'comment': comment
        }

        comment_put_endpoint = '/api/products/comments/' + str(comment_id)
        comment_put_url = base_url + comment_put_endpoint
        comment_put_response = requests.put(comment_put_url, data=comment_data, headers=headers)
        
        return comment_put_response


def comment_delete(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    comment_del_endpoint = '/api/products/comments/' + str(id)
    comment_del_url = base_url + comment_del_endpoint
    comment_del_response = requests.delete(comment_del_url, headers=headers)
    return comment_del_response