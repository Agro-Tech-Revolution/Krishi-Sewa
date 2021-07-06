
from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('login', login_view),
    path('register', register_view),
    path('history', history),
    path('feedback', feedback),
    path('add_production', add_production ),
    path('sell_product', sell_product),
    path('add_expenses', add_expenses),
    path('logout', logout_user),
    
]

