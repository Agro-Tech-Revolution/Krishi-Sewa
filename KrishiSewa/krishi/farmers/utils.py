import requests
import pickle
from rest_framework.response import Response
from api.views import *


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