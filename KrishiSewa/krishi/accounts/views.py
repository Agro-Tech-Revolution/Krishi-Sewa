from django.shortcuts import render, redirect
import requests
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .auth import *

# Create your views here.


@unauthenticated_user
def add_production(request):
    return render(request,'accounts/AddProduction.html')


@unauthenticated_user
def sell_product(request):
    return render(request,'accounts/SellProduct.html')


@unauthenticated_user
def add_expenses(request):
    return render(request,'accounts/AddExpenses.html')


@unauthenticated_user
def feedback(request):
    return render(request,'accounts/Feedback.html')


@unauthenticated_user
def history(request):
    return render(request,'accounts/History.html')

base_url = "http://127.0.0.1:8000"



@unauthenticated_user
def home(request):
    return render(request,'accounts/Home.html')

@unauthenticated_user
def login_view(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_data = {
            'username': username,
            'password': password
        }
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            auth_endpoint = "/auth/"
            auth_url = base_url + auth_endpoint
            
            r = requests.post(auth_url, data=user_data)
            if Response(r).status_code == 200:
                login(request, user)
                token = r.json().get('token')
                request.session['token'] = token
                if user.is_staff:
                    return redirect('/admins/')
                else:
                    headers = {'Authorization': 'Token ' + token}
                    profile_endpoint = "/api/profile/"
                    profile_url = base_url + profile_endpoint + str(user.id)

                    profile_response = requests.get(profile_url, headers=headers)
                    user_type = profile_response.json().get('user_type')
                    
                    if user_type.upper() == 'BUYERS':
                        return redirect('/buyers/')
                    elif user_type.upper() == 'FARMERS':
                        return redirect('/farmers/')
                    elif user_type.upper() == 'VENDORS':
                        return redirect('/vendors/')
            
        else:
            print("No user found")
        
    return render(request, 'accounts/login.html')


@unauthenticated_user
def register_view(request):
    if request.method=='POST':
        
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_type = request.POST.get('user_type')
        
        user_data = {
            "first_name": fname,
            "last_name": lname,
            "username": username,
            "email": email,
            "password": password
        }
        
        user_endpoint = "/api/users/"
        user_url = base_url + user_endpoint
        r = requests.post(user_url, data=user_data)
        if Response(r).status_code == 200:
            id = r.json().get('id')
            profile_data = {
                "user": id,
                "user_type": user_type
            }

            profile_endpoint = "/api/profile/"
            profile_url = base_url + profile_endpoint
            profile_request = requests.post(profile_url, data=profile_data)
            
            if Response(profile_request).status_code == 200:
                print("User successfully created")
                return redirect('/login')
        else:
            print("Error in creating user")

    return render(request, 'accounts/signup.html')


def logout_user(request):
    request.session.clear()
    logout(request)
    return redirect('/login')