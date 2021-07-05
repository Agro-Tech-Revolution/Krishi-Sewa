import requests
import pickle
from rest_framework.response import Response


base_url = "http://127.0.0.1:8000"

def comment_add(request):
    headers = {'Authorization': 'Token ' + request.session['token']}
    data = request.POST
    product = data['product']
    comment = data['comment']
    comment_by = request.user.id

    comment_data = {
        'comment_by': comment_by,
        'product': product,
        'comment': comment
    }

    comment_post_endpoint = '/api/productsOnSale/comments'
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

        comment_put_endpoint = '/api/productsOnSale/comments/' + str(comment_id)
        comment_put_url = base_url + comment_put_endpoint
        comment_put_response = requests.put(comment_put_url, data=comment_data, headers=headers)
        
        return comment_put_response


def comment_delete(request, id):
    headers = {'Authorization': 'Token ' + request.session['token']}

    comment_del_endpoint = '/api/productsOnSale/comments/' + str(id)
    comment_del_url = base_url + comment_del_endpoint
    comment_del_response = requests.delete(comment_del_url, headers=headers)
    return comment_del_response


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