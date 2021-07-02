from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *

# Create your views here.
@login_required
@farmers_only
def index(request):
    return render(request, 'farmers/farmers.html')

def image_test(request):
    return render(request, 'farmers/nav.html')