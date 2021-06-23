from django.shortcuts import render
from accounts.auth import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@buyers_only
def index(request):
    return render(request, 'buyers/buyers.html')