from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .auth import *
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required

# Create your views here.

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
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)

            request.session['token'] = token.key
            if user.is_staff:
                return redirect('/admins/')
            else:
                return redirect('/')
        else:
            print("No user found")
        
    return render(request, 'accounts/login.html')                        


# @unauthenticated_user
# def login_view(request):
#     if request.method== 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user_data = {
#             'username': username,
#             'password': password
#         }
#         user = authenticate(request,
#                             username=username,
#                             password=password)
#         if user is not None:
#             auth_endpoint = "/auth/"
#             auth_url = base_url + auth_endpoint
            
#             r = requests.post(auth_url, data=user_data)
#             if Response(r).status_code == 200:
#                 login(request, user)
#                 token = r.json().get('token')
#                 request.session['token'] = token
#                 if user.is_staff:
#                     return redirect('/admins/')
#                 else:
#                     headers = {'Authorization': 'Token ' + token}
#                     profile_endpoint = "/api/profile/"
#                     profile_url = base_url + profile_endpoint + str(user.id)

#                     profile_response = requests.get(profile_url, headers=headers)
#                     user_type = profile_response.json().get('user_type')
                    
#                     if user_type.upper() == 'BUYERS':
#                         return redirect('/buyers/')
#                     elif user_type.upper() == 'FARMERS':
#                         return redirect('/farmers/')
#                     elif user_type.upper() == 'VENDORS':
#                         return redirect('/vendors/')
            
#         else:
#             print("No user found")
        
#     return render(request, 'accounts/login.html')


@unauthenticated_user
def register_view(request):
    if request.method=='POST':
        
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_type = request.POST.get('user_type')
        
        request.data = {
            "first_name": fname,
            "last_name": lname,
            "username": username,
            "email": email,
            "password": password
        }
        
        user_obj = UserAPIView()
        user_response = user_obj.post(request)
        # user_endpoint = "/api/users/"
        # user_url = base_url + user_endpoint
        # r = requests.post(user_url, data=user_data)
        if user_response.data.get('id') != None:
            id = user_response.data.get('id')
            request.data = {
                "user": id,
                "user_type": user_type
            }
            print(request.data)
            profile_obj = CreateProfile()
            profile_response = profile_obj.post(request)

            # profile_endpoint = "/api/profile/"
            # profile_url = base_url + profile_endpoint
            # profile_request = requests.post(profile_url, data=profile_data)
            
            if profile_response.data.get('user') != None:
                print("User successfully created")
                return redirect('/login')
        else:
            print("Error in creating user")

    return render(request, 'accounts/register.html')


@login_required
def report_user(request, user_id):
    if request.method == 'POST':
        data = request.POST 
        reported_by = request.user.id
        reported_user = user_id
        report_category = data["report-category"]
        report_description = data["description"]

        request.data = {
            "reported_by": reported_by,
            "reported_user": reported_user,
            "report_category": report_category,
            "report_description": report_description,
        }
        
        report_user_obj = ReportUserView()
        report_user_response = report_user_obj.post(request)

        if report_user_response.data.get('id') != None:
            print("Reported Successfully")
        else:
            print(report_user_response.data)
    return redirect('/')


def logout_user(request):
    request.session.clear()
    logout(request)
    return redirect('/login')