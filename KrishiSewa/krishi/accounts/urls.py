
from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('history', history),
    path('login', login_view),
    path('register', register_view),
    path('logout', logout_user),
    
]

