from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('addProducts', add_products),
    
    
]