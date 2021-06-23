from django.shortcuts import render, redirect
import requests
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def login_view(request):
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        data = {
            'username': username,
            'password': password
        }
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            
            r = requests.post('http://127.0.0.1:8000/auth/', data=data)
            if Response(r).status_code == 200:
                login(request, user)
                token = r.json().get('token')
                request.session['token'] = token

                headers = {'Authorization': 'Token ' + token}
                profile_response = requests.get('http://127.0.0.1:8000/api/profile/'+str(user.id), headers=headers)
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
                
        r = requests.post('http://127.0.0.1:8000/api/users/', data=user_data)
        if Response(r).status_code == 200:
            id = r.json().get('id')
            profile_data = {
                "user": id,
                "user_type": user_type
            }
            profile_request = requests.post('http://127.0.0.1:8000/api/profile/', data=profile_data)
            if Response(profile_request).status_code == 200:
                print("User successfully created")
                return redirect('/')
        else:
            print("Error in creating user")

    return render(request, 'accounts/register.html')


def logout_user(request):
    request.session.clear()
    logout(request)
    return redirect('/')