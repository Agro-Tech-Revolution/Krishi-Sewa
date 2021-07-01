import os

import keras.models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from flask import Flask, request, render_template


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

    return crops[prediction]


def result(request):
    N = int(request.GET['N'])
    P = int(request.GET['P'])
    K = int(request.GET['K'])
    temp = int(request.GET['temp'])
    humidity = int(request.GET['humidity'])
    ph = int(request.GET['ph'])

    result = getNPK_Prediction(N, P, K, temp, humidity, ph)

    return render(request, 'farmers/npk_result.html', {'result': result})


def get_image_model(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    img_model = keras.models.load_model("SoilNet_93_86.h5")
    predict_crops = np.argmax(img_model.predict(image))

    classes = {0: "Alluvial Soil:-{ Rice,Wheat,Sugarcane,Maize,Cotton,Soyabean,Jute }",
               1: "Black Soil:-{ Virginia, Wheat , Jowar,Millets,Linseed,Castor,Sunflower} ",
               2: "Clay Soil:-{ Rice,Lettuce,Chard,Broccoli,Cabbage,Snap Beans }",
               3: "Red Soil:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }"}

    prediction = classes[predict_crops]

    return prediction


def predict(request):
    if request.method == 'POST':
        file = request.files['image']  # fet input
        filename = file.filename
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
        crop_predict = get_image_model(file_path)

        return redirect(request, {'result': crop_predict})
