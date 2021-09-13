from admins.api.views import TicketResponseView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .auth import *
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages


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
            messages.success(request, "User Logged in")
            if user.is_staff:
                return redirect('/admins/')
            else:
                
                return redirect('/')
        else:
            messages.error(request, "No user found")
        
    return render(request, 'accounts/login.html')  


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                print('User already activated')

            if user.is_active:
                return redirect('/login/')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
                
        except Exception as e:
            pass
        return redirect('/login/')                  

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
            "password": password,
            "is_active": False
        }
        
        user_obj = UserAPIView()
        user_response = user_obj.post(request)
        if user_response.data.get('id') != None:
            id = user_response.data.get('id')
            request.data = {
                "user": id,
                "user_type": user_type
            }
            profile_obj = CreateProfile()
            profile_response = profile_obj.post(request)
            
            if profile_response.data.get('user') != None:
                messages.success(request, 'User Created Successfully! \nActivate your account by clicking the link in your email.')                   
                return redirect('/login')
        else:
            messages.error(request, "Error in creating user")
            

    return render(request, 'accounts/signup.html')


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
            messages.success(request, "Reported Successfully")
        else:
            messages.error(request, report_user_response.data)
    return redirect('/')

@login_required
def send_response(request, ticket_id):
    if request.method == 'POST':
        data = request.POST
        response = data["response"]
        ticket = ticket_id
        response_by = request.user.id

        request.data = {
            "ticket": ticket,
            "response": response,
            "response_by": response_by,
        }

        ticket_response_obj = TicketResponseView()
        ticket_response_sent = ticket_response_obj.post(request)
        if ticket_response_sent.data.get('id') != None:
            messages.success(request, "Response submitted successfully")

        else:
            messages.error(ticket_response_sent.data)
    return redirect('/')

@login_required
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        request.data = {
            "old_password": data["old_password"],
            "new_password": data["new_password"]
        }
        change_psw_obj = ChangePasswordView()
        change_psw_response = change_psw_obj.put(request)
        if change_psw_response.data.get('message') != None:
            messages.success(request, change_psw_response.data.get('message'))
        else:
            messages.error(change_psw_response.data)
    return redirect('/')

def feedback(request):
    return render(request, 'accounts/user-feedback.html')

def submit_feedback(request):
    if request.method == 'POST':
        data = request.POST
        feedback_type = data["type"]
        name = data["name"]
        email = data["email"]
        description = data["description"]

        request.data = {
            "feedback_type": feedback_type,
            "name": name,
            "email": email,
            "description": description,
        }

        feedback_obj = FeedbackView()
        feedback_response = feedback_obj.post(request)
        if feedback_response.data.get('id') != None:
            messages.success(request, "Feedback Submitted Successfully")
        else:
            messages.error(request, feedback_response.data)
    return redirect('/')


def logout_user(request):
    request.session.clear()
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/login')