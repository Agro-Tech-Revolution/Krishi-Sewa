from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def index(request):
    print(request.session.get('token'))
    return HttpResponse("This is vendors page")