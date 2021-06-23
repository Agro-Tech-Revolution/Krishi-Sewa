from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    print(request.session.get('token'))
    return HttpResponse("This is buyers page")