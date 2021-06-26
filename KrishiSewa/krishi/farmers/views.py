from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
import pickle


# Create your views here.
@login_required
@farmers_only
def index(request):
    return render(request, 'farmers/farmers.html')


"""
Soil testing part -----------------------------------------
"""


def test(request):
    return render(request, 'farmers/index.html')


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


def result(request):
    N = int(request.GET['N'])
    P = int(request.GET['P'])
    K = int(request.GET['K'])
    temp = int(request.GET['temp'])
    humidity = int(request.GET['humidity'])
    ph = int(request.GET['ph'])

    result = getNPK_Prediction(N, P, K, temp, humidity, ph)

    return render(request, 'farmers/npk_result.html', {'result': result})
