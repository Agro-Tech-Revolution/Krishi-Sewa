from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.auth import *

# Create your views here.
@login_required
@vendors_only
def index(request):
    return render(request, 'vendors/vendors.html')