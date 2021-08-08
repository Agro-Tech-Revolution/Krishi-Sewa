from django.shortcuts import redirect
import requests
from api.views import *


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            token = request.session.get('token')
            id = request.user.id
            if request.user.is_staff:
                return redirect('/admins')

            elif not request.user.is_staff:
                profile = GetProfileType()
                profile_response = profile.get(request=request, user_id=id)
                user_type = profile_response.data["user_type"]
                if user_type.upper() == 'BUYERS':
                    return redirect('/buyers')
                elif user_type.upper() == 'FARMERS':
                    return redirect('/farmers')
                elif user_type.upper() == 'VENDORS':
                    return redirect('/vendors')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            token = request.session.get('token')
            id = request.user.id
            profile = GetProfileType()
            profile_response = profile.get(request=request, user_id=id)
            user_type = profile_response.data["user_type"]
            if user_type.upper() == 'BUYERS':
                return redirect('/buyers') 
            elif user_type.upper() == 'FARMERS':
                return redirect('/farmers')
            elif user_type.upper() == 'VENDORS':
                return redirect('/vendors')
            # return redirect('/users')
    return wrapper_function


def buyers_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admins')
            
        else:  
            id = request.user.id
            profile = GetProfileType()
            profile_response = profile.get(request=request, user_id=id)
            user_type = profile_response.data["user_type"]
            if user_type.upper() == 'BUYERS':
                # return redirect('/buyers')
                return view_function(request, *args, **kwargs)
            elif user_type.upper() == 'FARMERS':
                return redirect('/farmers')
            elif user_type.upper() == 'VENDORS':
                return redirect('/vendors')            
    return wrapper_function


# def farmers_only(view_function):
#     def wrapper_function(request, *args, **kwargs):
#         if request.user.is_staff:
#             return redirect('/admins')
            
#         else:
#             token = request.session.get('token')
#             id = request.user.id
          
#             headers = {'Authorization': 'Token ' + token}
#             profile_response = requests.get('http://127.0.0.1:8000/api/profile/'+str(id), headers=headers)
#             user_type = profile_response.json().get('user_type')
#             if user_type.upper() == 'BUYERS':
#                 return redirect('/buyers')
#             elif user_type.upper() == 'FARMERS':
#                 # return redirect('/farmers')
#                 return view_function(request, *args, **kwargs)
#             elif user_type.upper() == 'VENDORS':
#                 return redirect('/vendors')            
#     return wrapper_function

def farmers_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        
        if request.user.is_staff:
            return redirect('/admins')
        else:
            id = request.user.id
            profile = GetProfileType()
            profile_response = profile.get(request=request, user_id=id)
            user_type = profile_response.data["user_type"]

            if user_type.upper() == 'BUYERS':
                return redirect('/buyers')
            elif user_type.upper() == 'FARMERS':
                return view_function(request, *args, **kwargs)
            elif user_type.upper() == 'VENDORS':
                return redirect('/vendors')

    return wrapper_function

def vendors_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admins')
            
        else:
            
            id = request.user.id
            profile = GetProfileType()
            profile_response = profile.get(request=request, user_id=id)
            user_type = profile_response.data["user_type"]

            if user_type.upper() == 'BUYERS':
                return redirect('/buyers')
            elif user_type.upper() == 'FARMERS':
                return redirect('/farmers')
            elif user_type.upper() == 'VENDORS':
                # return redirect('/vendors')
                return view_function(request, *args, **kwargs)            
    return wrapper_function
